---
name: nivelamento
description: Deep, adaptive placement for the ai-engineering-from-scratch curriculum — picks a career route and scope, then binary-searches the learner's edge in each relevant strand (lesson-level, not phase-level), separates vocabulary from mechanism from practice, and writes a lesson-level study plan (LEARNING.md) plus a placement note in the vault. Resumable across sessions. Use for /nivelamento, "montar meu plano de estudos", "onde começo no currículo", "refazer o nivelamento".
argument-hint: "[continuar | refazer]"
---

# Nivelamento — find the edge, strand by strand

The goal is the same as `teach` Phase 1a, at curriculum scale: locate the **edge** of the learner's knowledge — the frontier where what they reliably know turns into what they don't — along every strand their goal depends on, **bracketed** (a floor they get right, a ceiling they miss). Ten fixed questions can't do that; this takes 30–50 adaptive questions, 40–70 minutes, and can be split across sessions.

The biggest risk for this learner: an AI engineering mentorship gives a lot of **vocabulary** and **practice** without necessarily the **mechanism**. A placement that rewards recognizing terms would skip exactly what they need. So: questions test *why / what happens if / which fails*, never *what is the name of*; and each strand gets judged on three levels.

Follow `teach` for everything about questions: one `quiz` per call (Bash `timeout: 600000`), options built with the construction procedure (parallel bare claims, real misconceptions, no tells), "Não sei" taken as a real gap. Talk in Brazilian Portuguese.

## Files

- `python3 .claude/tools/placement.py routes` — career routes and paths (from `curriculum/learning-paths/`).
- `python3 .claude/tools/placement.py strands --route <id>` — the 15 strands (`.claude/tools/strands.json`): ordered lessons per strand, dependencies, quiz stock per lesson, and which strands the route touches (**ROTA**), needs as foundation (**BASE da rota**) or doesn't need (**fora da rota**).
- `python3 .claude/tools/placement.py route-lessons <id>` — the route's own lesson sequence.
- **State lives in the vault note** `~/Documents/AI Engineering/Aulas/Nivelamento <YYYY-MM-DD>.md` (template below). Update its progress table after **every** answer — that's what makes the placement resumable.
- **Output**: that note (finished) + `LEARNING.md` at the project root.

## Routing

- `continuar` or an in-progress note exists (`status: em andamento` in `Aulas/Nivelamento *.md`) → read it, resume at the first strand not `concluída`.
- `refazer` or an old `LEARNING.md` exists → ask (AskUserQuestion): **refazer tudo** (archive `LEARNING.md` as `LEARNING-<date>.md`, keep its Progress log), **recalibrar algumas vertentes** (only the ones they pick), or **cancelar**. Never overwrite history silently. The queue may be an **integrated roadmap** (stages `### Etapa N` with `mentoria:` items and *Depois*): when recalibrating or redoing, keep the stages and the `mentoria:` items as they are, and only re-plan the curriculum lessons (update or move lessons inside stages and in *Depois*).
- Otherwise → Step 1.

## Step 1 — Goal, route and scope (AskUserQuestion; ~5 min)

1. **Mission** — why AI engineering, what they want to be able to build/do. Free text, keep their words.
2. **Route** — run `placement.py routes`, then present the career routes (by their `decisionPrompt`, in Portuguese) and recommend the one closest to the mission. A route is a ~12-lesson specialist sequence; the strands fill in what it rests on.
3. **Depth scope** — this learner wants mechanism depth, so ask explicitly:
   - **Rota + base** — only the strands the route touches and their dependencies.
   - **Rota + mecanismo de LLMs** *(recommend)* — also `representacao-texto`, `atencao-transformers`, `treino-llms` and their base (`algebra-linear`, `calculo-otimizacao`, `probabilidade`, `ml-classico`, `redes-neurais`) — understanding how the models work, not only how to use them.
   - **Tudo** — all 15 strands.
4. **Time per week** — only to phrase the pace honestly.
5. **Mentorship coverage** — read `Aulas/Mentoria/*/00 Visão geral.md` and grep `Fontes/Mentoria/` for each in-scope strand's `keywords`. Show which strands the mentorship has touched and ask them to add topics the transcripts don't show yet. Strands the mentorship covered get **mandatory mechanism questions** (Step 3c): that's where vocabulary can masquerade as understanding.

Create the note now (template at the end), fill *Objetivo*, and list the in-scope strands in dependency order (base → mecanismo → aplicação) in the progress table.

## Step 2 — Where to start each strand

Go strand by strand, **in dependency order** — a strand's result is only trustworthy once its `deps` are known. If a dependency came out weak, start the dependent strand lower (its edge is probably early too) but still probe it: practice can run ahead of foundations, and that gap is itself a finding.

Before the first question of a strand, glance at the vault: `Conceitos/` notes with `status: sólido` for the strand's topics are evidence for a higher start.

## Step 3 — Probe the strand (3–6 questions)

The strand's lessons `[0..n-1]` are ordered easy → hard. Keep `piso` (highest lesson index answered right; start at −1) and `teto` (lowest index missed; start at n).

**a. Binary search.** Ask about the middle lesson of (`piso`, `teto`):
- right → `piso` = that index; jump up sharply (don't inch forward);
- wrong or "Não sei" → `teto` = that index;
- stop when `teto − piso ≤ 1`, or after 5 search questions (then mark the gap between them as uncertain).
A run of all-correct means the questions were too easy — keep going up until something breaks or the strand runs out. If the strand runs out with everything right, the ceiling is beyond the curriculum: say so.

**b. Where each question comes from.**
- Lesson **with** a `quiz.json` (see `quiz:` in the strands listing): prefer a `post` question — it tests the lesson's content. The key stays inside the script:
  `python3 .claude/tools/quiz.py --lesson curriculum/phases/<lesson-id> --stage post --index <n>`
  Skip a repo question that only tests recognition of a term; write your own instead.
- Lesson **without** a quiz, or when the repo question is too shallow: read the lesson's `docs/en.md` (the core-concept and build-it sections) and write a **mechanism** question from it — a prediction ("o que acontece com X se…"), a failure ("qual destas mudanças quebra…"), a comparison ("por que A e não B…"), or a small computation. Pass `"topic": "<strand-id>"` and the lesson in `details` (`"Nivelamento · <strand> · <lesson-id>"`).
- Never two questions in a row from the same lesson during the search.

**c. Three levels.** Once the edge is bracketed:
- **Vocabulário** — implied by the search (recognition-level questions it passed).
- **Mecanismo** — ask **one** mechanism question at the floor lesson (the highest one they got right). Right → the floor stands. Wrong → the floor was vocabulary: lower `piso` to the last lesson with a mechanism-level pass and mark the strand **"vocabulário sem mecanismo"** for those lessons. Mandatory for strands the mentorship covered; optional otherwise (ask it when the search answers were recognition-level).
- **Prática** — ask once per strand, with AskUserQuestion (no right answer): *já construí isso em projeto real / já fiz em exercício ou na mentoria / só li ou ouvi falar / nunca vi*. Practice never moves the floor — it changes *how* those lessons are taught later (faster, anchored in what they built).

**d. Wrong answers are data.** A wrong pick (not "Não sei") of a specific distractor may be a held misconception. Ask **one** follow-up around it before moving on. If confirmed, write it under *Concepções erradas* in the note — `teach` must dislodge it, not just top it up.

**e. Optional open question** for the 2–3 strands most central to the route: at the edge, ask in chat for a 2–4 sentence explanation ("Explique por que dividimos por $\sqrt{d_k}$ na atenção"). Before reading the answer, decide in your reasoning the 2–3 points a correct explanation must contain; grade against them, tell the learner which points were present/missing, and record it. Don't use it to move the floor by itself — only to confirm or question the search result.

**f. Record** after every answer: update the strand's row (piso, teto, perguntas, mecanismo, prática) and, at the end of the strand, its result:
- **Dominada** — floor at the last lesson, mechanism confirmed.
- **Borda em `[k]`** — entry lesson = `teto` (the first lesson missed).
- **Vocabulário sem mecanismo** — entry lesson = the lowest lesson that failed the mechanism check.

Keep going strand by strand. Offer a pause between strands ("faltam N vertentes, ~X min — continuar agora ou depois?"); a pause is safe because the note holds the state.

## Step 4 — Build the plan

**Per lesson status**, for every in-scope strand:
- lessons **below the floor**, mechanism confirmed → **Pular**;
- floor-region lessons passed only at vocabulary level, or right in the search but never mechanism-checked → **Confirmar** (run only the lesson's post-quiz / a mechanism check before skipping it in `/curriculo`);
- lessons from the entry point up → **Fazer**.

**Study queue**: one ordered list mixing strands, respecting `deps` — base before mechanism before application, and inside that the route's own order (`placement.py route-lessons`) for route lessons. Strands the learner already handles in practice but lacks mechanism go early: that's the highest-value gap. Lessons outside every in-scope strand (rest of the curriculum) are **Fora do escopo** — reachable later with `/guia-curso`.

**Hours**: sum the queue's minutes (route lessons have `minutes`; for others, use the per-lesson average the strands listing reports).

Present in chat: the strand map (mermaid, see note template), the top findings (biggest gaps, misconceptions, vocabulary-without-mechanism), and the first 10 lessons of the queue. Ask for adjustments (AskUserQuestion), then write the files.

## Step 5 — Write the outputs

**`LEARNING.md`** at the project root (exactly these sections — `/curriculo` and `/prova-fase` read them):

~~~markdown
# My AI Engineering Path
<!-- Managed by /nivelamento and /curriculo. Placement note: Aulas/Nivelamento <date>.md -->

## Mission
<their words> · Route: <route id — title> · Scope: <rota + base | rota + mecanismo | tudo>

## Placement
- Date: <YYYY-MM-DD>
- Method: adaptive, <N> questions across <M> strands
- Pace: ~<hours>/week
- Estimated: ~<H> h for the study queue

## Strands
| Strand | Result | Entry lesson | Mechanism | Practice |
|--------|--------|--------------|-----------|----------|

## Study queue
<!-- /curriculo takes the first unchecked item. "confirmar" = post-quiz / mechanism check only. -->
- [ ] <phase-dir>/<lesson-dir> — <title> · <strand> · fazer
- [ ] <phase-dir>/<lesson-dir> — <title> · <strand> · confirmar

## Path
| Phase | Name | Status | Est. hours |
|-------|------|--------|------------|
<all 20 phases; Status: Do (has queued "fazer" lessons), Review (only "confirmar" lessons), Skip (in scope, all skipped), Out of scope>

## Progress log
| Date | Lesson | Quiz | Note |
|------|--------|------|------|

## Review queue
~~~

When **recalibrating** some strands: update only those rows and their queue items; keep the Progress log and checked items.

**The vault note**: finish it (*Resultado*, *Mapa*, *Concepções erradas*, *Plano*), set `status: concluída`. Add the misconceptions and vocabulary-without-mechanism topics to the *Fila de aprofundamento* in `00 Mapa.md`, and fill its *Trilha — Currículo* table with the queue's phases. **Do not** create or mark concept notes as `sólido`: placement is evidence, not teaching — `sólido` only comes from `teach`.

Close in three lines: the entry point of the queue, total hours, and that `/curriculo` starts it (and that `/nivelamento refazer` can recalibrate some strands when they feel the plan drifting).

## Note template

~~~markdown
---
tags: [nivelamento]
data: <YYYY-MM-DD>
status: em andamento
rota: <route id>
escopo: <rota + base | rota + mecanismo | tudo>
---
# Nivelamento <YYYY-MM-DD>

## Objetivo
<missão nas palavras do aprendiz> · Rota: <título> · Escopo: <…> · Ritmo: ~<h>/semana
Mentoria já cobriu: <vertentes / temas>

## Progresso
| Vertente | Piso | Teto | Perguntas | Mecanismo | Prática | Resultado |
|---|---|---|---|---|---|---|
| algebra-linear | −1 | 7 | 0 | — | — | pendente |

## Mapa
```mermaid
graph TD
  %% uma caixa por vertente, setas = deps; rótulo = resultado ("dominada", "borda: <aula>", "vocab sem mecanismo")
```

## Concepções erradas
- <vertente> — <o que o aprendiz acredita> vs <o correto> (pergunta de <data>)

## Vocabulário sem mecanismo
- <tema> — reconhece o termo, não explicou o porquê

## Perguntas abertas
- <pergunta> — pontos presentes / ausentes

## Plano
<resumo: primeiras aulas da fila, horas, observações>
~~~
