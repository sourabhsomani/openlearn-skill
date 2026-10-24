#!/usr/bin/env python3
"""Build a spaced, interleaved revision calendar up to an exam.

Each concept gets a strength: weak | ok | strong. Weak concepts are reviewed more often
at expanding intervals; strong ones less. Sessions mix several concepts (interleaving).
The day before the exam is reserved for a mixed mock test.

Usage:
    python study_schedule.py --exam 2026-11-20 [--start 2026-10-26] \
        --concepts "Osmosis:weak" "Diffusion:ok" "Cell wall:strong" \
        [--minutes 45] [--max-per-day 4] [--format markdown|json|ics] [-o plan.md]

Concepts may also come from a file: --concepts-file concepts.txt (one "Name:strength" per line).
"""
import argparse
import datetime as dt
import json
import sys
import uuid

# Review offsets (days after the concept is first studied), expanding like Leitner boxes.
OFFSETS = {
    "weak":   [0, 1, 3, 7, 14, 30, 60],
    "ok":     [0, 3, 8, 18, 40],
    "strong": [0, 10, 30],
}
STRENGTHS = ("weak", "ok", "strong")


def parse_concepts(items):
    concepts = []
    for raw in items:
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        name, _, strength = raw.rpartition(":")
        if not name or strength.strip().lower() not in STRENGTHS:
            name, strength = raw, "ok"
        concepts.append((name.strip(), strength.strip().lower()))
    return concepts


def build_plan(concepts, start, exam, max_per_day):
    total_days = (exam - start).days
    if total_days < 1:
        sys.exit("The exam date must be after the start date.")
    mock_day = total_days - 1            # day index of the mock test (exam eve)
    review_days = max(mock_day, 1)       # reviews happen on days [0, review_days)

    # Compress the schedule if the window is short, keeping the expanding shape.
    longest = max(OFFSETS["weak"][:5])
    scale = min(1.0, (review_days - 1) / longest) if review_days > 1 else 0.0

    # Weak concepts first so they are introduced earliest; stagger introductions.
    order = sorted(concepts, key=lambda c: STRENGTHS.index(c[1]))
    stagger_span = max(1, min(4, review_days // 4))
    days = {d: [] for d in range(review_days)}

    for i, (name, strength) in enumerate(order):
        first = i % stagger_span
        hits = set()
        for off in OFFSETS[strength]:
            d = first + round(off * scale) if scale < 1 else first + off
            if d < review_days:
                hits.add(d)
        # Make sure weak/ok concepts get a review close to the exam.
        if strength in ("weak", "ok") and review_days > 2:
            late = review_days - (1 if strength == "weak" else 2)
            if not any(h >= late - 3 for h in hits):
                hits.add(late)
        for d in sorted(hits):
            days[d].append((name, strength, d == first))

    # Spread overloaded days to the next lighter day (never past the review window).
    for d in range(review_days):
        while len(days[d]) > max_per_day:
            # move the strongest, non-introduction item forward
            # never move a first-study item: its later reviews are anchored to it
            movable = [x for x in days[d] if not x[2]]
            if not movable:
                break
            item = sorted(movable, key=lambda x: -STRENGTHS.index(x[1]))[0]
            target = next((t for t in range(d + 1, review_days) if len(days[t]) < max_per_day), None)
            if target is None:
                break
            days[d].remove(item)
            days[target].append(item)

    plan = []
    for d in range(review_days):
        if days[d]:
            plan.append({"date": (start + dt.timedelta(days=d)).isoformat(), "type": "review",
                         "items": [{"concept": n, "strength": s, "first_study": f} for n, s, f in days[d]]})
    plan.append({"date": (start + dt.timedelta(days=mock_day)).isoformat(), "type": "mock",
                 "items": [{"concept": n, "strength": s, "first_study": False} for n, s in order]})
    return plan


def to_markdown(plan, minutes, exam, max_per_day):
    lines = [f"# Revision plan (exam {exam.isoformat()})", "",
             "Each session: answer questions from memory first, check, then fix gaps. "
             "Mix the topics within a session rather than doing them one block at a time.", "",
             "| Date | Day | Session | Focus |", "|---|---|---|---|"]
    for s in plan:
        d = dt.date.fromisoformat(s["date"])
        if s["type"] == "mock":
            lines.append(f"| {s['date']} | {d:%a} | Mock test ({minutes} min) | "
                         "Timed mixed test on all topics, then review every mistake |")
            continue
        parts = []
        for it in s["items"]:
            tag = "learn + quiz" if it["first_study"] else "retrieval quiz"
            mark = " ⚠️" if it["strength"] == "weak" else ""
            parts.append(f"{it['concept']}{mark} ({tag})")
        n = len(s["items"])
        sess = f"{minutes} min" if n == 1 else f"{minutes} min (~{max(5, minutes // n)} min each)"
        lines.append(f"| {s['date']} | {d:%a} | {sess} | {'; '.join(parts)} |")
    lines += ["", "⚠️ = weak concept: spend the most time here. If you get a topic wrong in a session, "
              "add an extra review of it the next day."]
    if any(len(x["items"]) > max_per_day for x in plan if x["type"] == "review"):
        lines.append(f"Note: some days have more than {max_per_day} topics because the time to the exam is short. "
                     "Consider longer sessions or prioritizing the ⚠️ topics.")
    return "\n".join(lines)


def to_ics(plan, minutes):
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//OpenLearn//Study Schedule//EN", "CALSCALE:GREGORIAN"]
    for s in plan:
        d = dt.date.fromisoformat(s["date"])
        nxt = d + dt.timedelta(days=1)
        if s["type"] == "mock":
            summary = "OpenLearn: Mock test (all topics)"
            desc = f"Timed mixed test, about {minutes} min. Review every mistake afterwards."
        else:
            summary = "OpenLearn: " + ", ".join(i["concept"] for i in s["items"])
            desc = "Retrieval practice: answer from memory first, then check. " + "; ".join(
                f"{i['concept']} ({i['strength']})" for i in s["items"])
        desc = desc.replace(",", "\\,").replace(";", "\\;")
        summary = summary.replace(",", "\\,").replace(";", "\\;")
        out += ["BEGIN:VEVENT", f"UID:{uuid.uuid4()}@openlearn", f"DTSTAMP:{stamp}",
                f"DTSTART;VALUE=DATE:{d:%Y%m%d}", f"DTEND;VALUE=DATE:{nxt:%Y%m%d}",
                f"SUMMARY:{summary}", f"DESCRIPTION:{desc}", "END:VEVENT"]
    out.append("END:VCALENDAR")
    return "\r\n".join(out) + "\r\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--exam", required=True, help="exam date YYYY-MM-DD")
    ap.add_argument("--start", default=dt.date.today().isoformat(), help="first study day (default today)")
    ap.add_argument("--concepts", nargs="*", default=[], help='"Name:weak|ok|strong" ...')
    ap.add_argument("--concepts-file")
    ap.add_argument("--minutes", type=int, default=45, help="minutes per day")
    ap.add_argument("--max-per-day", type=int, default=4)
    ap.add_argument("--format", choices=["markdown", "json", "ics"], default="markdown")
    ap.add_argument("-o", "--output")
    args = ap.parse_args()

    items = list(args.concepts)
    if args.concepts_file:
        with open(args.concepts_file, encoding="utf-8") as f:
            items += f.read().splitlines()
    concepts = parse_concepts(items)
    if not concepts:
        sys.exit("Give at least one concept with --concepts or --concepts-file.")

    start, exam = dt.date.fromisoformat(args.start), dt.date.fromisoformat(args.exam)
    plan = build_plan(concepts, start, exam, max(1, args.max_per_day))

    if args.format == "json":
        text = json.dumps({"exam": exam.isoformat(), "minutes_per_day": args.minutes, "sessions": plan}, indent=2)
    elif args.format == "ics":
        text = to_ics(plan, args.minutes)
    else:
        text = to_markdown(plan, args.minutes, exam, max(1, args.max_per_day))

    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        print(f"Wrote {len(plan)} sessions to {args.output}")
    else:
        print(text)


if __name__ == "__main__":
    main()
