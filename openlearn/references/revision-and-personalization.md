# Personalized revision

Revision should target what *this* learner gets wrong, spaced over time, mixed rather
than blocked. Re-reading the chapter is the thing to replace.

## Step 1: Diagnose

Sources of evidence, in order of reliability:
1. Their answers to OpenLearn quizzes/tutor sessions (tagged by concept and Bloom's level).
2. Their own marked test papers or mistakes they share.
3. Self-report ("I don't get titration"). Useful, but confirm it with 2–3 diagnostic
   questions, since people often misjudge what they know.

Classify each error, because each type needs a different fix:

| Error type | Signal | Fix |
|---|---|---|
| **Knowledge gap** | Doesn't recall the fact/definition | Flashcards + retrieval drills |
| **Misconception** | Confident, consistent wrong idea | Explicit contrast ("You think X; actually Y because…"), then "spot the mistake" items |
| **Procedural slip** | Right method, wrong execution (units, signs, steps) | Faded worked examples, checklists |
| **Application gap** | Knows it, can't use it in new situations | Varied scenario problems, interleaved practice |
| **Exam technique** | Knows it, loses marks on structure/wording | Model answers + marking guides |

## Step 2: Build a revision set

For each weak concept, produce a short targeted block:
- A 3–5 line re-explanation from a *different angle* than before (new analogy, diagram or
  example). Repeating the same explanation rarely helps.
- 3–5 retrieval questions at increasing difficulty, including one "why" and one
  application question.
- For misconceptions: one "Spot the mistake" or "True/False and justify" item.

Then add an **interleaved mixed set** of 6–10 questions that mixes the weak concepts with
some strong ones and different problem types, so the learner practises *choosing* the
right method, not just executing it. Revision questions must be new, not repeats of quiz
items the learner has already seen with answers.

## Step 3: Schedule (spacing)

### Leitner boxes (simple and transparent)

| Box | Review after | Moves when… |
|---|---|---|
| 1 | 1 day | correct → box 2 |
| 2 | 3 days | correct → box 3 |
| 3 | 7 days | correct → box 4 |
| 4 | 14 days | correct → box 5 |
| 5 | 30 days | correct → stays (mastered) |

Any wrong answer → back to box 1. New or weak concepts start in box 1; concepts answered
correctly on the first quiz start in box 2.

### Exam-date plans

When the learner has an exam date, run the scheduler:

```bash
python scripts/study_schedule.py --exam 2026-11-20 --start 2026-10-26 \
  --concepts "Osmosis:weak" "Cell membrane:ok" "Mitochondria:strong" \
  --minutes 45 --format markdown
```

It spaces reviews more densely for weak concepts, interleaves topics within each session,
leaves the final day for a mixed mock test, and can output markdown, JSON or an `.ics`
calendar file (`--format ics -o plan.ics`) the learner can import into Google Calendar.
Explain the plan in one or two sentences; don't just dump it.

If the exam is very close (≤3 days), skip spacing and prioritize: highest-weight topics ×
weakest concepts, mixed retrieval practice, one timed mock, and sleep.

## Progress file

When file tools are available, keep `openlearn-progress.json` in the working folder so the
next session can continue. Read it at the start of a session if it exists; update it after
each quiz or tutor session.

```json
{
  "learner": {"level": "Class 10 CBSE", "goal": "Board exam", "exam_date": "2027-03-01",
              "language": "English", "preferences": "likes real-life examples"},
  "subjects": {
    "Biology — Ch5 Cell Structure": {
      "source": "NCERT Class 9 Biology Ch5",
      "concepts": {
        "Osmosis": {"box": 1, "attempts": 4, "correct": 1,
                    "error_types": ["misconception"],
                    "notes": "thinks solute moves, not water",
                    "last_reviewed": "2026-10-25", "next_review": "2026-10-26"},
        "Mitochondria": {"box": 3, "attempts": 3, "correct": 3,
                         "last_reviewed": "2026-10-25", "next_review": "2026-11-01"}
      },
      "sessions": [{"date": "2026-10-25", "mode": "quiz", "score": "7/10"}]
    }
  }
}
```

Without file tools, keep a short **"Your progress"** block at the end of a session that the
learner can paste into the next chat, and suggest they enable memory or keep the block.

## Starting a returning session

If progress exists, open with a quick warm-up: 3–5 questions on concepts due for review
today (spaced retrieval) *before* new material. Then: "You've improved on X. Y is still
tricky. Want to work on Y or move on to the next chapter?"
