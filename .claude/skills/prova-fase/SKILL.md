---
name: prova-fase
description: Phase quiz for the ai-engineering-from-scratch curriculum — tests a whole completed phase. Use for /prova-fase <fase>, "me testa na fase N", "estou pronto para a próxima fase?".
argument-hint: "<número ou nome da fase>"
---

# Prova de fase

Read `curriculum/skills/check-understanding/SKILL.md` and follow it, with these overrides:

- Lessons and their `quiz.json` are in `curriculum/phases/`; never fetch from GitHub.
- Every question goes through the quiz popup — for questions taken from a lesson's `quiz.json`, use lesson mode so the answer key never appears in the command:
  `python3 .claude/tools/quiz.py --lesson curriculum/phases/<phase>/<lesson> --stage <stage> --index <n>` (Bash `timeout: 600000`). Use `--count` to see what each lesson has. Questions you write yourself go through the stdin spec, following the `teach` option rules.
- Phases with few or no `quiz.json` (2, 3, 6, 7, 8, 9, 10, 11, 12, 15, 16): write the questions yourself from the lessons' `docs/en.md` — mechanism-level (predict / what breaks / why A not B), one per main lesson, following the `teach` option rules.
- Talk in Brazilian Portuguese.
- Results: record the score in `LEARNING.md` *Progress log* (and lessons that clearly failed back into *Study queue* as `fazer`), and for each concept missed set its `Conceitos/` note in the vault to `status: revisar` and add the miss under *Erros que eu cometi*.
- Next actions: `/curriculo` (never the repo's `learn`), `/guia-curso`.
