# Learning science behind OpenLearn

Use this to make design choices and, when a learner or teacher asks "why are you making me
do this?", to explain briefly.

## The evidence base

**Dunlosky et al. (2013), "Improving Students' Learning With Effective Learning
Techniques"** (Psychological Science in the Public Interest, 14(1)) reviewed ten common
study techniques:

| Utility | Techniques |
|---|---|
| **High** | Practice testing (retrieval practice), distributed practice (spacing) |
| **Moderate** | Elaborative interrogation, self-explanation, interleaved practice |
| **Low** | Summarization, highlighting/underlining, keyword mnemonic, imagery for text, rereading |

Key nuance: for practice testing, the benefit comes from actually *retrieving* the answer
from memory. Looking it up or flipping the card immediately gives little benefit. Hence:
answers come after attempts.

**Worked-example effect / cognitive load theory (Sweller; Renkl).** Novices learn
procedures faster by studying worked solutions than by struggling with problems alone,
because problem-solving overloads working memory. The transition to independence works
best with **faded examples**: later examples leave steps blank for the learner, usually the
last steps first ("backward fading"). Self-explanation prompts inside examples add further
benefit. As expertise grows, worked examples stop helping (expertise reversal), so fade
faster for stronger learners.

**Spaced repetition (Leitner 1972; Wozniak's SM-2, 1987; FSRS).** Reviewing at expanding
intervals counters the forgetting curve. Leitner boxes are a simple, transparent
approximation: correct → move up a box (longer interval), wrong → back to box 1.

**Twenty rules of formulating knowledge (Wozniak, 1999).** The most important for card
writing: (1) don't learn what you don't understand, (2) learn before you memorize,
(4) minimum information principle (atomic items), (5) cloze deletion, (9–10) avoid sets
and long sequences, (11) combat interference between similar items, (14) personalize and
give examples, (18) provide sources.

**Multiple-choice item writing (Haladyna, Downing & Rodriguez, 2002).** One concept per
item; the stem should be answerable without seeing options; plausible distractors drawn
from common errors; homogeneous options; avoid "all/none of the above", negatives, and
clues like grammatical mismatches or the longest option being correct.

**Revised Bloom's taxonomy (Anderson & Krathwohl, 2001).** Remember → Understand → Apply →
Analyze → Evaluate → Create. Use it to make sure questions go beyond recall.

**AI tutoring research (LearnLM / Eedi RCT, 2025).** Socratic questioning from a
pedagogically tuned model was effective, but tutors noted students got frustrated when
questioning persisted too long. Lesson: guide with questions, but give a direct explanation
after two unsuccessful attempts or when the learner asks.

## Principle → feature mapping

| Principle | How OpenLearn applies it |
|---|---|
| Retrieval practice | Check-your-understanding questions in lessons; quizzes; flashcards; answers hidden until attempted |
| Spacing | Revision plans and `study_schedule.py`; Leitner boxes in the progress file |
| Interleaving | Revision quizzes mix concepts and problem types instead of blocking by topic |
| Elaborative interrogation | "Why is this true?" / "What would happen if…?" prompts in lessons and the tutor |
| Self-explanation | Worked examples ask the learner to justify steps |
| Worked/faded examples | Example sequences in `lessons-and-examples.md` |
| Feedback | Every answer key explains why the right answer is right and why each distractor is wrong |
| Learn before memorizing | Lesson comes before flashcards in the Study Pack; cards only cover understood material |
| Desirable difficulty | Questions should feel slightly hard; aim for ~70–85% success in practice |
| Low-utility techniques | Summaries are used only as a scaffold ("Chapter at a glance"), never as the main study tool |
