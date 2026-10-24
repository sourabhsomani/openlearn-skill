# OpenLearn: Personal AI Tutor Skill

OpenLearn turns any textbook chapter, lecture notes, PDF or document into **lessons,
worked examples, quizzes, flashcards and personalized revision exercises**, built on
proven learning science.

**Who benefits:** students, teachers and self-learners.

It's an open **SKILL.md** skill — the same `openlearn/` folder works in ChatGPT, GitHub
Copilot and Claude without any changes. What differs is only how each platform lets you
install and share it.

## What it does

Share your study material and ask in plain language. OpenLearn reads it, maps the key
concepts and the mistakes students commonly make, asks up to three quick questions about
you, then produces any of these modes:

| Mode | Example request |
|---|---|
| **Study Pack** (default) | "Help me study this chapter" |
| **Lesson** | "Explain chapter 4 simply" |
| **Worked Examples** | "Show me how to solve these numericals step by step" |
| **Quiz** | "Make a 15-question quiz from these notes" |
| **Flashcards** | "Flashcards from this PDF for Anki" |
| **Personalized Revision** | "I got these questions wrong, help me revise" |
| **Tutor Session** | "Quiz me one question at a time" |
| **Teacher Mode** | "Make a Class 8 worksheet with an answer key" |

## Why it works

Every mode makes the learner *recall and apply* rather than reread:

- **Retrieval practice and spacing**: the two study techniques rated "high utility" in
  Dunlosky et al. (2013). Quizzes hide answers until attempted; revision is spaced.
- **Atomic flashcards and cloze deletions**: following Wozniak's *20 rules of formulating
  knowledge*.
- **Quiz items with plausible distractors built from real misconceptions**: following
  Haladyna, Downing & Rodriguez (2002) item-writing guidelines; every answer key explains
  why each wrong option is wrong.
- **Worked → faded examples**: from cognitive load theory (Sweller, Renkl).
- **Socratic tutoring that knows when to just explain**: after two failed attempts, the
  tutor gives a clear explanation instead of more questions.
- **Faithful to your source**: your textbook's definitions and notation win; anything added
  from outside is labelled *"Beyond the text"*.

---

## Installation & Usage by Platform

The `openlearn/` folder uses the open **SKILL.md** format. ChatGPT, GitHub Copilot and
Claude all read it — you don't change anything in the folder. The steps below only differ
in how each platform loads and shares it.

---

### ChatGPT

**Who can use it**

Native skill upload is available on **ChatGPT Business, Enterprise, Healthcare and Edu**
plans only, if a workspace admin has skills turned on. Free and Plus accounts cannot add
skills inside ChatGPT itself — but OpenAI's coding tool **Codex** also reads SKILL.md
skills, so Codex users can follow the same steps.

**How to add it**
1. Zip the `openlearn/` folder:
   ```bash
   git clone https://github.com/sourabhsomani/openlearn-skill.git
   cd openlearn-skill
   zip -r openlearn.zip openlearn/
   ```
2. In ChatGPT go to **Skills → Create → Upload from your computer** and upload `openlearn.zip`
3. ChatGPT scans every upload — it may mark the skill **"Needs Review"** or block it if
   something looks risky. If that happens, contact your workspace admin.

**How to share it**
- **Share link** — use the Share button to send it to specific people or copy a link
- **Publish to workspace** — if your admin allows it, publish it so everyone in your org can use it
- **Public reach** — OpenAI does not have a public skill store; point the general public to
  this GitHub repo instead

**Use it**

Open a chat with the skill active, attach your study material, and prompt:

> "Make a 10-question quiz from this chapter. I'm preparing for a college entrance exam."

> "Create Anki flashcards from these lecture notes."

---

### GitHub Copilot

Copilot reads SKILL.md files from well-known folder paths. Pick the scope that fits.

**Per-project (one repository)**

Put the folder at `.github/skills/openlearn/` inside the repo:
```bash
mkdir -p .github/skills
cp -r openlearn .github/skills/openlearn
```
Copilot also checks `.claude/skills/` and `.agents/skills/` in the same repo.

**For yourself across all projects (global)**

Copy the folder to your home skills directory:
```bash
# macOS / Linux
cp -r openlearn ~/.copilot/skills/openlearn

# Windows (PowerShell)
Copy-Item -Recurse openlearn "$env:USERPROFILE\.copilot\skills\openlearn"
```

**Installing from this repo (one command)**

Anyone can install the skill directly from GitHub using the `gh` CLI:
```bash
gh skill add https://github.com/sourabhsomani/openlearn-skill
```
The same `gh skill` command can search for, update and remove skills, and lets you publish
your own to the community. To get noticed, submit to the
[Awesome GitHub Copilot](https://github.com/github/awesome-copilot) community list.

**Use it in Copilot Chat**

Open the Copilot Chat panel (`Ctrl+Shift+I`), paste or attach your material, and ask:

> "Use the OpenLearn tutor. Here are my notes — make me a quiz."

> "Give me spaced flashcards for these definitions."

---

### Claude

**Claude.ai (web, desktop, mobile)**
1. Zip the `openlearn/` folder (see the ChatGPT step above for the zip command)
2. In Claude go to **Customize → Skills → + → Upload a skill** and upload the ZIP

Teams and Enterprise accounts can also use **Share** and **Publish to org** so everyone in
the organisation gets access. You can submit the skill to Anthropic's public directory for
wider listing.

**Claude Code (CLI)**

Copy the folder into Claude Code's skills directory:
```bash
git clone https://github.com/sourabhsomani/openlearn-skill.git
cp -r openlearn-skill/openlearn ~/.claude/skills/
```

Claude Code picks up `SKILL.md` automatically in every new session. To activate it
explicitly, type `/openlearn` in the chat.

**Use it**

Start a new chat, attach or paste your study material, and prompt:

> "Teach me this chapter. I'm in Class 10 and my exam is on 20 November."

If the skill doesn't activate on its own, add *"use the OpenLearn skill"* to your message.

---

### Google Gemini (Gems)

Gemini supports **Gems** — custom AI experts defined by a system prompt.

**Create the Gem**
1. Go to [gemini.google.com](https://gemini.google.com) and click **Gem manager → New Gem**
2. **Name:** OpenLearn Tutor
3. **Instructions:** paste the full contents of [openlearn/SKILL.md](openlearn/SKILL.md)
4. Optionally paste in any of the `references/` files for deeper detail on quiz rules,
   flashcard formats, etc.

**Use it**

Open your OpenLearn Gem, attach or paste your study material, and prompt:

> "Here are my biology notes. Create a study pack. I have an exam in 3 weeks."

> "Give me worked examples for each formula in this chapter."

> "Make cloze flashcards I can import into Anki."

Gemini 1.5 Pro and 2.0 can handle long PDFs natively — attach the file directly for best
results.

**Google AI Studio (developers / API)**

For iterating on the prompt or running via API:
1. Go to [aistudio.google.com](https://aistudio.google.com) → **Create new prompt → System instructions**
2. Paste the contents of `openlearn/SKILL.md`
3. Paste or upload your study material in the user turn
4. Run with Gemini 1.5 Pro or Gemini 2.0 Flash

---

### One repo, every platform

GitHub is the single public home for OpenLearn. Every platform installs from the same
`openlearn/` folder — no duplicates, no diverging versions. Share this repo URL and each
person installs into whichever tool they use.

---

## Included tools

Both scripts need only Python 3 (no extra packages).

**Anki export**: flashcards JSON → import-ready Anki text file (Basic + Cloze cards):
```bash
python openlearn/scripts/export_anki.py cards.json -o my_deck.txt
```

**Study schedule**: spaced, interleaved revision calendar up to an exam (markdown, JSON
or `.ics` for Google Calendar):
```bash
python openlearn/scripts/study_schedule.py --exam 2026-11-20 \
  --concepts "Osmosis:weak" "Diffusion:ok" "Cell wall:strong" --format ics -o plan.ics
```

---

## Structure

```
openlearn/
├── SKILL.md                         # core workflow and modes
├── references/
│   ├── learning-science.md          # evidence base, principle → feature map
│   ├── lessons-and-examples.md      # lessons, worked & faded examples
│   ├── quiz-design.md               # question types, Bloom's mix, MCQ rules
│   ├── flashcards.md                # card rules, cloze, Anki export
│   ├── revision-and-personalization.md  # error analysis, Leitner, progress file
│   ├── tutor-session.md             # interactive Socratic sessions
│   └── teacher-mode.md              # worksheets, differentiation, lesson plans
├── scripts/
│   ├── export_anki.py
│   └── study_schedule.py
└── assets/
    └── study-pack-template.md
```

---

## Contributing

Issues and pull requests are welcome, especially:
- question styles for specific exam boards (CBSE, ICSE, IB, AP, GCSE, JEE/NEET…)
- support for more languages
- example study packs for different subjects

---

## References

- Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013).
  Improving Students' Learning With Effective Learning Techniques. *Psychological Science
  in the Public Interest*, 14(1), 4–58.
- Wozniak, P. (1999). *Effective learning: Twenty rules of formulating knowledge.*
- Haladyna, T. M., Downing, S. M., & Rodriguez, M. C. (2002). A review of multiple-choice
  item-writing guidelines. *Applied Measurement in Education*, 15(3), 309–334.
- Renkl, A., Atkinson, R. K., Maier, U. H., & Staley, R. (2002). From example study to
  problem solving: Smooth transitions help learning. *Journal of Experimental Education*.
- Anderson, L. W., & Krathwohl, D. R. (2001). *A Taxonomy for Learning, Teaching, and
  Assessing.*

---

## License

[MIT](LICENSE)
