---
name: revisar-desenho
description: Review a from-memory Excalidraw drawing the learner made — look at the exported PNG, compare it with the lesson's dependency map and sources, point out what's right, missing and wrong, quiz any misconception, and record the result in the vault. Use for /revisar-desenho, "terminei o desenho", "revisa meu desenho".
argument-hint: "[nome do desenho]"
---

# Revisar desenho

## 1. Find and look at the drawing

```bash
python3 .claude/tools/drawing.py find $ARGUMENTS
```

It prints the drawing note, its exported PNG, the frontmatter (`aula`, `conceitos`) and the typed text elements.

- **PNG found** → open it with the Read tool and **actually look at it**. Handwriting, arrows, boxes, crossings-out — read all of it. If something is illegible, ask what it says instead of guessing.
- **PNG marked stale or missing** → ask the learner to export (Excalidraw: *Auto-export PNG* setting, or the export button → save to vault) and stop until they confirm. Never review from the typed text alone: the drawing is the hand-drawn part.

## 2. Get the reference

Read the lesson note in `aula` (its dependency map, the unfolded explanation, the sources) and the concept notes in `conceitos`. The map is the reference for **structure**; the sources (mentor passages, curriculum lesson) are the reference for **facts**. When unsure whether something drawn is true, check the source or ask the `researcher` — don't judge from memory.

## 3. Compare — structure first

Judge the drawing as a dependency graph, not as art:

- **Correto** — nodes and edges that are right. Say specifically what's right; it reinforces it.
- **Faltando** — nodes or edges from the map that aren't there. A missing *edge* (two things drawn but not connected) is as important as a missing node: it's a fact held without its reason.
- **Errado** — an arrow in the wrong direction, a relation that's false, a step in the wrong order, a mislabeled part. These are misconceptions: the most important finding.
- **Além do mapa** — things they added that are right but weren't taught: credit them.

Don't nitpick drawing quality, spelling or layout.

## 4. Act on it

- For each **errado**: don't just correct it — run one `quiz` that targets that misconception (built per the `teach` option rules) to see if it's a slip or a held belief, then fix it with a short motivate → establish → connect.
- For each **faltando** that matters: one quick question or a two-line reminder of *why* it's there (the edge, not just the node).
- Then offer, without pressure: redraw now, redraw in a few days (spaced), or move on.

## 5. Record in the vault

- Drawing note: set `revisado: true` in the frontmatter (edit only the frontmatter line — never touch the `## Drawing` JSON or text elements).
- Lesson note, under *Desenho*: keep the embed and add a short *Revisão do desenho* (data, correto / faltando / errado in one or two lines each).
- Concept notes: misconceptions under *Erros que eu cometi* (with the date); status — a correct drawing of a node that already passed its quiz-check can move it to `sólido`; a wrong edge moves it to `revisar`.
- `00 Mapa.md`: update the concepts-by-status lists if a status changed.
