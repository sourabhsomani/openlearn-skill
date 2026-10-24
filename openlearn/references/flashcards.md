# Flashcards

Flashcards are for retaining what the learner already understands. Make them after the
lesson, not instead of it.

## Rules for good cards (adapted from Wozniak's 20 rules)

1. **One fact per card (minimum information principle).** Short question, even shorter
   answer. If an answer has "and" in it, it's probably two cards.
   - ✗ Q: What are the features of the Dead Sea? A: salt lake on the Israel–Jordan border,
     lowest point on land, only simple organisms…
   - ✓ Q: The Dead Sea lies on the border of which two countries? A: Israel and Jordan
   - ✓ Q: Why can only simple organisms live in the Dead Sea? A: its very high salt content
2. **Use cloze deletions** for definitions and key sentences:
   "Photosynthesis takes place in the {{c1::chloroplasts}}."
3. **Avoid unordered sets and long lists.** "Name the 7 features of…" is a poor card.
   Split into cloze cards, or use one card per item with a context cue, or give a
   mnemonic for a short ordered list.
4. **Ask in both directions when useful:** term → definition and definition → term
   (e.g. vocabulary, formulas ↔ what they calculate).
5. **Include "why" cards**, not just "what" cards. Cause/mechanism cards build
   understanding: "Why does ice float on water?"
6. **Combat interference.** Similar items (mitosis/meiosis, affect/effect, adapt/adopt) get
   cards that ask for the *distinguishing* feature, so the learner doesn't mix them up.
7. **Context cues** keep wording short: prefix with a topic tag, e.g. "[Chem · Acids]".
8. **Personal examples help:** "Example of inertia you see daily?" is better than abstract.
9. **Source reference** on the back (section/page) so the learner can go back.
10. **Prioritize.** Cover the core concepts first; mark nice-to-know cards with a tag.

## Quantity

Roughly 15–30 cards per chapter section; scale to density. Vocabulary/biology/history
chapters need more; conceptual physics needs fewer cards but more "why" cards.

## Presenting in chat

```
| # | Front | Back | Tag |
|---|---|---|---|
| 1 | [Bio · Cells] Organelle where aerobic respiration happens? | Mitochondrion | core |
| 2 | Photosynthesis takes place in the ____. | chloroplasts | core |
```

Or front/back pairs if the table would be too wide. Offer: "Want me to quiz you on these
one at a time?" That turns them into a tutor session with real retrieval.

## Anki / spaced repetition export

When the learner uses Anki (or wants a file), write the cards to JSON and run the export
script:

```json
{
  "deck": "Biology::Ch5 Cell Structure",
  "cards": [
    {"front": "Organelle where aerobic respiration happens?", "back": "Mitochondrion",
     "tags": ["cells", "core"], "source": "Section 5.2"},
    {"cloze": "Photosynthesis takes place in the {{c1::chloroplasts}}.",
     "tags": ["cells"]}
  ]
}
```

```bash
python scripts/export_anki.py cards.json -o biology_ch5_anki.txt
```

The output is a UTF-8 tab-separated text file with Anki file headers (`#separator:tab`,
`#html:true`, `#notetype column`, `#deck column`, `#tags column`), so Basic and Cloze cards
import together and land in the right deck. Tell the learner: *Anki → File → Import →
choose the file → check the preview → Import.* The same file also works in most apps that
accept tab-separated front/back text (they'll ignore the header lines or let you skip them).
