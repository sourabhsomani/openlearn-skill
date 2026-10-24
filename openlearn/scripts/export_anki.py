#!/usr/bin/env python3
"""Convert OpenLearn flashcards (JSON) into an Anki-importable text file.

Input JSON:
{
  "deck": "Biology::Ch5 Cell Structure",          # default deck (optional)
  "cards": [
    {"front": "...", "back": "...", "tags": ["a"], "source": "Sec 5.2"},   # Basic card
    {"cloze": "The {{c1::nucleus}} holds DNA.", "extra": "...", "tags": []}, # Cloze card
    {"front": "...", "back": "...", "reverse": true}                         # Basic + reversed
  ]
}

Output: UTF-8, tab-separated, with Anki 2.1.54+ file headers so Basic and Cloze notes
import together into the right deck(s):
    notetype <TAB> deck <TAB> field1 <TAB> field2 <TAB> tags

Usage:
    python export_anki.py cards.json -o deck.txt [--deck "Name"] [--raw-html]
"""
import argparse
import csv
import html
import json
import re
import sys

CLOZE_RE = re.compile(r"\{\{c\d+::")


def clean(text, raw_html):
    """Make a field safe for a single tab-separated line with #html:true."""
    if text is None:
        return ""
    text = str(text).strip()
    if not raw_html:
        text = html.escape(text, quote=False)
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")
    return text.replace("\t", "    ")


def clean_tags(tags):
    if isinstance(tags, str):
        tags = tags.split()
    out = []
    for t in tags or []:
        t = re.sub(r"\s+", "_", str(t).strip())
        if t:
            out.append(t)
    return " ".join(out)


def build_rows(data, default_deck, raw_html):
    rows, problems = [], []
    deck_fallback = default_deck or data.get("deck") or "OpenLearn"
    for i, card in enumerate(data.get("cards", []), start=1):
        deck = card.get("deck") or deck_fallback
        tags = clean_tags(card.get("tags"))
        source = card.get("source")

        if "cloze" in card:
            text = card["cloze"]
            if not CLOZE_RE.search(text or ""):
                problems.append(f"card {i}: cloze text has no {{{{c1::...}}}} deletion; skipped")
                continue
            extra = card.get("extra", "")
            if source:
                extra = f"{extra}\n(Source: {source})" if extra else f"(Source: {source})"
            rows.append(["Cloze", deck, clean(text, raw_html), clean(extra, raw_html), tags])
            continue

        front, back = card.get("front"), card.get("back")
        if not front or not back:
            problems.append(f"card {i}: needs both 'front' and 'back' (or 'cloze'); skipped")
            continue
        if source:
            back = f"{back}\n(Source: {source})"
        notetype = "Basic (and reversed card)" if card.get("reverse") else "Basic"
        rows.append([notetype, deck, clean(front, raw_html), clean(back, raw_html), tags])
    return rows, problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="flashcards JSON file")
    ap.add_argument("-o", "--output", default="openlearn_anki.txt")
    ap.add_argument("--deck", help="override the default deck name")
    ap.add_argument("--raw-html", action="store_true",
                    help="card text already contains intended HTML; don't escape < > &")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        data = {"cards": data}

    rows, problems = build_rows(data, args.deck, args.raw_html)
    if not rows:
        sys.exit("No valid cards found. " + " ".join(problems))

    with open(args.output, "w", encoding="utf-8", newline="") as f:
        f.write("#separator:tab\n#html:true\n#notetype column:1\n#deck column:2\n#tags column:5\n")
        writer = csv.writer(f, delimiter="\t", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writerows(rows)

    basic = sum(1 for r in rows if r[0].startswith("Basic"))
    print(f"Wrote {len(rows)} cards ({basic} basic, {len(rows) - basic} cloze) to {args.output}")
    for p in problems:
        print("warning:", p)


if __name__ == "__main__":
    main()
