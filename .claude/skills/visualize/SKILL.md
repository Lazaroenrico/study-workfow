---
name: visualize
description: "Add a correct, minimal visual to a lesson — a diagram or geometric picture — that renders in the Obsidian vault. Use when an idea is genuinely clearer as a picture: a dependency graph, system/flow, sequence, state machine, tree, comparison, or a spatial/geometric thing (coordinate geometry, number line, vectors, a plot, a physical layout). Simple diagrams go inline as Mermaid; spatial ones (and diagrams that must be visually verified) go to a maker subagent that renders, looks at the result, and publishes a PNG."
---

# Visualize

A picture earns its place only when it shows something words can't — shape, structure, direction, relationship, geometry. This skill produces ONE such picture, makes sure it is **correct**, and puts it in the lesson so it renders in the vault (the lesson note, and the session log via md-log).

You are the **creative director**. You decide the exact idea and distill it to its fewest carrying elements.

## When to visualize (and when not to)

This teaching system builds a **dependency graph in the learner's head** — unconditional truths at the root, derived facts hanging off them. A visual is powerful exactly when it makes that structure (or a geometry) visible. Reach for one when:

- The idea is a **structure or relationship**: dependencies, a system with parts and arrows, a flow/pipeline, a sequence of exchanges, a state machine, a tree/hierarchy, a comparison, a containment (what's inside vs outside).
- The idea is **spatial or geometric**: coordinate geometry, a number line, vectors, a function's shape, a physical arrangement.

Do NOT visualize when prose or a single equation already carries it. A decorative diagram that just restates the sentence next to it adds noise and a chance to be wrong. When in doubt, don't — a missing visual is cheaper than a false one.

And never right before a `/desenho`: the learner draws from memory first; the visual is the reference *after*.

## Choose the route

| The idea is… | Route |
|---|---|
| Nodes-and-edges, small (≤ ~7 nodes), simple layout — e.g. the lesson's dependency map | **Inline Mermaid**: write a ```` ```mermaid ```` block directly in your reply / the note. Obsidian renders it; free and instant. |
| Nodes-and-edges where layout or correctness is delicate (crossing arrows, a sequence with many exchanges, a state machine), or it will be reused | **`mermaid-maker`** subagent |
| Positions-and-shapes / geometry (vectors, plots, number lines, layouts) | **`svg-maker`** subagent |

Inline Mermaid hasn't been looked at: keep it simple enough that its correctness is obvious from the source (direction of every arrow, every label). If you can't tell from the source, use the maker.

## Brief the maker well: one idea, fewest elements

The most common failure is **cramming** — every extra label makes the picture harder to read AND harder to lay out correctly. Before briefing, prune to the fewest elements that carry the idea, and for each ask: *"if I delete this, is the idea still clear?"* If yes, delete it.

Give the maker the concept AND the concrete elements you want — not a vague topic, and not a long checklist.

- BAD: "make a diagram about how TCP works"
- GOOD: "graph TD: a node 'pacote' at the top; arrows down to 'ordenação' and 'retransmissão em perda'; both arrows down into 'stream confiável'. No title. Show that reliability is built FROM packets, not alongside them."

Keep the idea intact but trust the maker to compose; if your brief lists more than ~5–7 elements, cut it first.

## Invoke

Use the Agent tool with `subagent_type: "mermaid-maker"` or `"svg-maker"` and your brief as the prompt. The maker authors the source, renders it, **looks at the PNG and iterates until it is correct and clean**, publishes it into the vault's `viz/` with a unique filename, and returns:

```
RESULT:
filename: viz-<slug>-<timestamp>.png
path: ~/Documents/AI Engineering/viz/viz-<slug>-<timestamp>.png
```

If it returns `RESULT: NONE`, it couldn't make a correct picture of the brief — simplify or rethink, or decide the visual isn't worth it. Never fake a maker's output; correctness depends on its render-and-inspect loop.

## Embed it

Use Obsidian's embed with the returned **filename** (not the full path) and a display width:

```
![[viz-<slug>-<timestamp>.png|500]]
```

Put it in your reply (md-log mirrors it into the session note) and in the lesson note / concept note where it belongs. Obsidian resolves the embed by filename anywhere in the vault. Width `|500` is a good default; larger for dense diagrams. Introduce the visual in a sentence, then let it carry the idea — don't narrate every element back in prose.
