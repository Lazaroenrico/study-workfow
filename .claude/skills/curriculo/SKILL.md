---
name: curriculo
description: Study a lesson of the ai-engineering-from-scratch curriculum (cloned in curriculum/) with the teach method — the next lesson from LEARNING.md or a named one — and consolidate it into the vault. Use for "próxima aula do currículo", "continuar o curso", "estudar a aula X do currículo", or /curriculo.
argument-hint: "[fase/aula | tema]"
---

# Currículo — one curriculum lesson, taught with `teach`

The curriculum (`curriculum/`, a clone of rohitg00/ai-engineering-from-scratch) gives **mechanism** depth: the math, the from-scratch code, why it works. The mentorship gives **practice** depth. This skill runs one lesson through the `teach` method and consolidates it into the vault. Follow `teach` for everything; this skill only adds the curriculum specifics. It replaces the repo's own `learn` skill — never use that one.

## Lesson layout

`curriculum/phases/<NN-phase>/<NN-lesson>/`:
- `docs/en.md` — the lesson text (problem → concept → build it from scratch → use the library → quiz → artifact)
- `code/` — implementations (`main.py`, sometimes `.ts`/`.rs`/`.jl`); run from the `curriculum/` root
- `quiz.json` — questions with `stage`: `pre` (before), `check` (during), `post` (after)
- `assets/` — figures (often SVG); `outputs/` — the reusable artifact the lesson produces

Phase lists: `curriculum/README.md` (Contents) and `curriculum/phases/<phase>/README.md`.

## Step 0 — Which lesson

Argument: `$ARGUMENTS`

- **A lesson path or name** → that lesson (search `curriculum/phases/*/` directory names).
- **A topic** → find the lesson that covers it (see `/guia-curso`), confirm with the learner.
- **Empty** → read `LEARNING.md` (project root) and take the first unchecked item of *Study queue*. Items marked `confirmar` get only Step 5's post-quiz (or, without a quiz, 2–3 mechanism questions from the lesson): pass → check it off and log it as confirmed; miss → change it to `fazer` and teach it now. The queue is an **integrated roadmap** (stages `### Etapa N`) that also holds mentorship items, `- [ ] mentoria: <módulo> — <triagem | blocos a–b> · mentoria · …`: if the first unchecked item is one of those, say so and run the `mentoria` skill for that module and block range instead (it checks the item off). Only skip past it when the learner explicitly asked for a curriculum lesson; then take the first unchecked curriculum item. Older `LEARNING.md` files without a *Study queue*: the next lesson is the first not-yet-logged lesson of the first phase whose Status is `Do` or `Review`. No `LEARNING.md` → offer `/nivelamento` (adaptive placement + plan) or start at Phase 1, Lesson 1 — never block on setup.

**Lessons without `quiz.json`.** Many lessons have none — whole phases (2 ML, 3 Deep Learning, 6, 8, 9, 10 LLMs from Scratch, 12, 15) and most of 7 and 11. There, every quiz in this skill (warm-up, `pre`, `check`, `post`) is written by you from `docs/en.md`, following the `teach` option rules, as mechanism questions (predict / what breaks / why A not B / small computation) — never "what is X called". Aim for 2 before, 1 per main section during, 3–4 after. `quiz.py --lesson … --count` exits with an error when there's no `quiz.json`; that's the signal.

## Step 1 — Gather sources

- Read `docs/en.md` in full, and the main code file(s).
- Grep the mentorship transcripts (`~/Documents/AI Engineering/Fontes/Mentoria/`) and `Aulas/Mentoria/` for the lesson's key terms — when the mentor covered this, those passages (with `^p` links) are the practice side and the best **motivation**.
- Read the related `Conceitos/` notes in the vault (status, past mistakes).
- `python3 .claude/tools/quiz.py --lesson <lesson-dir> --count` to see how many questions each stage has.

## Step 2 — Probe

Warm-up: if a previous lesson is logged in `LEARNING.md`, ask 1–2 of its `post` questions first (retrieval after a gap).

Then `teach` Phase 1, starting with the lesson's own `pre` questions — one call each:

```bash
python3 .claude/tools/quiz.py --lesson curriculum/phases/<phase>/<lesson> --stage pre --index 0
```

(Bash `timeout: 600000`.) The answer key stays inside the script. Then add your own questions to bracket the edge, as `teach` requires — the curriculum's ordering already covers most prerequisites, so keep this shorter than for a free topic unless the `pre` answers reveal a gap. Do a full probe at the start of a new phase.

## Step 3 — Plan

`teach` Phase 2: the dependency map of this lesson. The curriculum's mechanism establishes the nodes; the mentor's passages (if any) motivate them. Present and wait for the go-ahead.

## Step 4 — Teach

`teach` Phase 3, following the lesson's own arc (problem → concept → build → library), each node through motivate → establish → connect → quiz-check:

- **Math**: derive step by step in LaTeX; ask for the next step when the learner can predict it.
- **Build it**: the learner types the important code — it's the repo's own rule ("type and build", not decoration). Their code goes in `pratica/<phase>/<lesson>/` in this project (never inside `curriculum/`, so `git pull` stays clean). Walk the reference code in 5–15 line chunks: what it does, why it exists, one prediction question. Run it from `curriculum/` and show the real output.
- **Use it**: the production library version — ask what the library does for them that the scratch version made explicit.
- **Quiz-checks**: use the lesson's `check` questions (`--stage check --index N`) at the matching points, plus your own.

## Step 5 — Post-quiz and record

- Every `post` question (`--stage post --index N`), one per call. Score = correct/total.
- `LEARNING.md`: check the lesson off in *Study queue* (wherever it sits — a stage or *Depois*); append a row to *Progress log* (date, `<phase>/<lesson>`, score, one line on what was hard). Score < 70% → add to *Review queue* with the missed topic. Last queued lesson of a phase → set the phase Status to `Done` and suggest `/prova-fase <phase>`.

## Step 6 — Consolidate

`teach` Phase 4, with the lesson note at `Aulas/Currículo/<NN-phase>/<NN-lesson>.md` (template `Templates/Aula.md`, `fonte: currículo`). Include:
- links to the original: `https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/<phase>/<lesson>` and `https://aiengineeringfromscratch.com/lesson?path=phases/<phase>/<lesson>`;
- the key code, short, in a code block (or a link to the learner's file in `pratica/`);
- figures from `assets/` worth keeping: copy them to the vault's `viz/` as `curriculo-<lesson>-<name>.<ext>` and embed `![[...|500]]`.

In concept notes, curriculum content goes under *Mecanismo*; add `"currículo <phase>/<lesson>"` to `fontes:`. Update the *Trilha — Currículo* table in `00 Mapa.md`.

Close in two lines: what they can now build or explain, and the next lesson's title as a hook. Suggest `/desenho` for the main idea.
