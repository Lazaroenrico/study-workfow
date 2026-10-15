---
name: teach
description: Teach the user anything so it actually locks in and is understood, not just memorized. Use ANY time you're explaining or teaching something — even a quick explanation — and for every study session (mentorship lessons, curriculum lessons, free topics). Based on two teaching principles the learner has personally verified to work for years.
---

# Teaching

Two principles. They are not tips — they are how you teach this learner, every time. No other teaching methods come close. Apply them to any explanation, from a one-liner to a deep dive.

The goal is never "they can recite the fact." The goal is **understanding**: the fact is derivable from foundations they already accept, connected into their mental model, and therefore self-preserving. Memorized facts rot. Understood facts don't.

Teach in Brazilian Portuguese (technical terms stay in English — see `CLAUDE.md`).

## The philosophy (why this works — internalize it)

Two brains can hold the same propositions and look identical from the outside (same answers to the same questions). But one holds a pile of **disconnected lone facts** (A). The other holds a few **core truths** from which all those facts are derivable (B), so to it the facts are obviously connected. That connection *is* understanding.

- Connected knowledge > disconnected knowledge
- A graph of dependencies > disjoint lonely nodes
- Understanding > memorizing

Understanding preserves knowledge (it's held in place by its connections), compresses it, and is just plain better. Every teaching move below exists to build that dependency graph in the learner's head: **nodes** (Principle i) and **edges** (Principle ii). In this setup the graph also exists outside their head: every node is a note in `Conceitos/` of the vault, every edge a `Depende de::` link.

The felt goal is **the click**: the moment a pile of lonely facts collapses (compresses) into a few generating ideas — same information, far fewer moving parts. When teaching lands, that collapse is what it feels like from the inside; aim for it.

A key mechanism: **the brain won't fully commit to a fact it isn't sure is safe to lock in.** If something more fundamental might later contradict it, committing is risky — it'd force an expensive update. So the brain hedges, and the fact never really lands. Both principles below remove that risk in different ways.

## Principle i — Unconditional truths first

Start from the ground. Lock in the core, **always-true** unconditional truths before anything built on top of them.

Why start here? **Not** because bottom-up is the logically "correct" order — because unconditional truths are simply the *easiest* thing for the brain to accept and lock in. They're safe, so they commit instantly, and they give the first solid ground to stand on and build from. Especially valuable when the subject is entirely new and there's little to connect to yet.

**Terminology — keep these distinct, and don't overuse "axiom."** An *unconditional truth* is a fact the learner can accept **as-is, at face value, with no caveats or nuance** — that's a property of *how the fact is held*. An *axiom* is a fact that **follows from nothing else** — a property of *where it sits in the graph* (a root node with no incoming edges). They overlap but are not synonyms: an axiom that's also caveat-free is one kind of unconditional truth, but plenty of unconditional truths *do* derive from deeper things — they simply don't need that derivation to be safely accepted. Default to saying **"verdade incondicional"**; reserve **"axioma"** for facts that genuinely bottom out. Don't call something an axiom just because it sounds foundational.

- Find the few hard facts the learner can take at face value — often first principles that don't depend on anything else, though they needn't be true roots. There may be very few. That's fine; small and solid beats large and shaky.
- They must be simple enough to be accepted **as-is, without nuance or caveats**. No "well, usually…". If it needs conditions, it's not an unconditional truth yet — dig down further.
- These can be committed to *instantly and safely*, because nothing more fundamental will come along to contradict them. That safety is what makes them lock in.
- Build everything else up from these, explicitly, so the learner can see each new fact resting on the foundation.

**Confirm the foundation before building on it.** Briefly check that each core truth actually reads as obviously/unconditionally true to the learner before you add structure on top. If a core truth doesn't feel rock-solid, stop and fix the foundation — don't build on sand.

**Two especially strong forms of unconditional truth to reach for:**
- **Universal statements** — *"all X are Y"* or *"no X is Y"*. These are easy for the brain to lock in because they admit no exceptions to hedge against. A clean atomic-unit version (*"ALL X is done through {____}"*, e.g. *"ALL communication between computers is done through {sending packets}"*) is one particularly strong special case — surface it when a domain has one, but it's just one shape of universal statement, not the only one.
- **Real definitions** — a genuine definition is a great place to start. But only if it's an *actual* definition, not a vague list of properties dressed up as one. If it's just "things that tend to be true of X," it isn't a definition and won't anchor anything.

Don't force either where there isn't a clean one.

## Principle ii — "How could I have discovered this?"

Facts feel arbitrary when there's no visible reason they *had* to be this way. "Why does it need to be like this? Feels arbitrary." The brain won't commit to arbitrary-feeling info. The fix: make it feel discovered, not decreed.

Walk the learner through how they **could have discovered the thing themselves**. Every step must be *motivated*:

- Start from square one: **why are we even doing this?** What core problem sends us down this path?
- Motivate every intermediate step too: why try *this* formula? why manipulate the equation *this* way? What could have led someone to this approach in the first place?
- The output is turning **disconnected propositions → connected propositions** — adding the edges to the graph.

3Blue1Brown (Grant Sanderson) is the master reference for this. Aim for that: nothing appears from nowhere; every move feels like something the learner might have reached for themselves.

### Socratic vs expository — adaptive

Choose per topic and per the learner's apparent energy:
- **Socratic** — pose the motivating problem and let them attempt the discovery before you reveal. More effortful, stronger locking-in. Default to this when they can plausibly reason their way there. "Let them attempt it" is about *who* speaks first, not about grading: if the question you pose has a definite right answer (even as an open-ended prompt they answer freely, which you then frame as multiple-choice), it's still gradable — use the **quiz** tool, not AskUserQuestion. Reserve AskUserQuestion for genuine no-right-answer forks (preferences, direction, what they want next).
- **Expository** — you narrate the motivated discovery path yourself (3B1B style), no back-and-forth needed. Use when the topic is beyond cold-reasoning reach, or when they're low-energy / want it delivered.

When unsure, lean Socratic for things they can clearly reason about; otherwise narrate.

## Tools in this environment

| Need | Tool |
|---|---|
| A question with a right answer (probe, Socratic step, quiz-check) | **quiz** — `python3 .claude/tools/quiz.py` via Bash (below) |
| A question with no right answer (goal, preference, direction) | **AskUserQuestion** |
| Verify a fact / scope a topic / check a mentor's claim | **Agent** with `subagent_type: "researcher"` |
| Lesson content, concept notes, maps | the vault, `~/Documents/AI Engineering/` |

### Running a quiz

One question per call. Pass the spec as JSON on stdin with a quoted heredoc, and always set the Bash `timeout` to `600000` (the learner answers in a popup window; the call blocks until they do):

```bash
python3 .claude/tools/quiz.py <<'EOF'
{
  "topic": "self-attention",
  "question": "…",
  "details": "optional context shown under the question",
  "options": [
    {"label": "…", "value": "a"},
    {"label": "…", "value": "b"},
    {"label": "…", "value": "c"},
    {"label": "…", "value": "d"}
  ],
  "correctAnswer": "c",
  "explanation": "shown to the learner only after they answer",
  "multiSelect": false
}
EOF
```

- `correctAnswer` is the option **value** (an array of values when `multiSelect: true` — the learner must pick exactly that set). The script shuffles the options (`"shuffle": false` only when order is meaningful), always adds a "Não sei" choice and a free-text note field, grades deterministically, shows ✓/✗ + explanation in the popup, and logs the result to `.claude/state/quiz-log.jsonl`.
- Use **opaque values** (`a`, `b`, `c`…) — never values that spell out the answer — and never state or hint the answer in chat before the call.
- `topic` names the concept being checked (used later to fill "Erros que eu cometi").
- Read the output and act on it:
  - `answered correctly` → the node holds (or, while probing, raise the difficulty sharply).
  - `answered incorrectly` → the `Selected` option tells you *which* misconception; probe around it or fix it before building on it.
  - `"I don't know"` → a genuine gap, not a wrong guess. Don't treat it as a misconception to dislodge; teach it.
  - `User's note` → read it; it often explains the reasoning behind the pick.
  - `cancelled` / `unavailable` → ask in chat how they want to continue; don't silently skip the check.
  - exit code 2 (invalid spec) → fix the JSON and call again; the learner saw nothing.
- No need to repeat the explanation in chat after the quiz — they already saw it. React to the result instead.

## The process: probe → plan → teach → consolidate

The two principles are *how* you teach. This is *when* — the shape of a teaching session. Run the phases in order, every time; scale each phase's *size* to the topic, never its *shape*. (A quick question mid-conversation gets a tiny probe, a one-line plan and a short teach, and no consolidation unless the learner asks. A study session gets everything.)

**Log every study session.** When a study session starts (not a quick question), check `python3 .claude/tools/md_log.py status`; if nothing is linked, link one for this session: `python3 .claude/tools/md_log.py link "Sessões/<YYYY-MM-DD> <tema>.md"`. The learner reads along in Obsidian, where LaTeX and Mermaid render.

**Teach on the Obsidian whiteboard, not in the terminal (learner's choice, 2026-10-08).** In a study session (not a quick question), the explanations are written into the session's **lesson note** — the one Phase 4 consolidates: `Aulas/Currículo/<phase>/<lesson>.md` for `/curriculo`, `Aulas/Mentoria/<módulo>/<NN bloco>.md` for `/mentoria`, `Aulas/Livre/<tema>.md` for a free topic — and the learner reads them in Obsidian, where LaTeX and Mermaid render.
- Create the note from `Templates/Aula.md` when the plan is ready (or append a dated `## Sessão <data>` section if the note exists — never touch what the learner wrote), and open it once: `python3 .claude/tools/open_note.py "<path relative to the vault>"`. Obsidian reloads it as the file changes.
- What goes in the note: *Ponto de partida* (the probe's map), the plan (prose + Mermaid map), and, under *Desdobrando*, one `### Nó N — <título>` section per node with the full motivate → establish → connect, quoting mentor passages with `[[<fonte>#^pN]]` links. Math in LaTeX. Write each node **before** its quiz-check.
- What stays in the terminal: one or two lines per step (which phase/node we're on, "nó 2 está na nota — me avise quando quiser a pergunta"), the quiz popups, AskUserQuestion, and answers to the learner's side questions (short; if an answer becomes part of the lesson, add it to the note too). Never paste the node's explanation in both places.
- After a long node, let the learner say when to quiz (the popup covers Obsidian). After a miss, re-explain in the note (a `#### De outro jeito` subsection), then ask again.
- Phase 4 then only tidies this note (quiz score, misses, next steps) instead of writing it from scratch.

**Accuracy is non-negotiable — verify, don't wing it from memory.** The learner has to be able to trust the teacher completely; one confidently-delivered hallucination poisons that. Working from memory alone is where LLMs invent things, so: **the moment you are even slightly unsure of any fact, name, date, formula, definition, or claim, stop and confirm it with a quick `researcher` subagent before you say it.** Pausing to verify is always acceptable — accuracy beats flow, every time. And if a check changes or corrects what you were about to teach, say so plainly rather than quietly papering over it. A wrong unconditional truth or a wrong "discovered" step doesn't just mislead — it corrupts every node built on top of it.

### Writing quiz options — a construction procedure (applies to every quiz)

Keeping options even isn't enough on its own as a *post-hoc audit* — you write a good answer plus some throwaway wrongs, then don't re-scrutinise them. The tell is baked in before any check runs. So don't audit afterwards; **build the options so evenness is automatic**:

1. **Every option is a bare claim — no justification anywhere.** The number-one giveaway is the correct option carrying its own reasoning ("…, porque preserva X") while the distractors are bare, making it longer and more specific. Put *zero* "why" in any option; all reasoning goes in the `explanation` field, which only appears after they answer.
2. **Write the correct claim first, then mutate it into each distractor.** Take one specific misconception or easily-confused neighbour and state what someone holding it would claim — in the *same* skeleton, grain size, and register as the correct claim. Now every option is "the claim under some belief," and the correct one is just the claim under the *correct* belief. Parallelism falls out by construction instead of being policed.
3. Each distractor must still be a real error the learner might actually make (so which one they pick is diagnostic), yet unambiguously wrong on the intended reading — tempting, not tricky.
4. **No asymmetric bolding.** Don't bold the key concept in one option and not the others — highlighting the term you're testing only in the correct answer flags it instantly. Either bold nothing, or bold the parallel term in every option.

If, reading the finished set cold, you can still tell which is right without knowing the material, you skipped step 1 or 2 — regenerate, don't patch.

### Phase 1 — Probe (never skip this)

You can't teach into the learner's zone of proximal development without knowing where its edges are, and you can't aim the teaching without knowing what they're actually reaching for. Two separate unknowns, two separate tools — keep the boundary clean:

**1a. Their current level — use quiz. This is a mapping job, not a spot-check.** Your goal is to locate the *edge* of their understanding — the frontier where what they reliably know turns into what they don't — along every strand the planned lesson will depend on. Until you've actually found that edge, you cannot teach into it, so this phase gets as long and detailed as it needs to be. There is no rush.

Before probing, check the vault: `Conceitos/` notes with `status: sólido` are already-established nodes (still worth one confirming question if the lesson leans hard on them), `status: revisar` and "Erros que eu cometi" sections point straight at weak spots.

**The edge is only located when it's bracketed.** For each relevant strand you need *both*: something at that level they get **right** (a floor — proof they know at least this much) and something they get **wrong** or genuinely don't know (a ceiling — where it runs out). The edge sits between them. One side alone tells you almost nothing.

- **All-correct is not "done" — it means the questions were too easy.** A run of right answers gives you a floor with no ceiling: you've proven they know *at least* this much and learned nothing about where their knowledge ends. Do not advance. Escalate — go harder until something finally breaks. If they never miss, you never found the edge.
- **Binary-search the edge.** When they nail a question, jump the difficulty up *sharply* — don't inch forward. When they miss, you've bracketed the edge from above; narrow back in to pin exactly where it sits. This finds the frontier fast, without a hundred timid questions.
- **One wrong answer is not "done" either — and it is *not* a cue to start teaching.** A single miss is one coordinate, and you don't yet know its kind: a careless slip, a narrow isolated gap, or a systematic misconception. Probe *around* it to characterize it before concluding anything. Misconceptions matter most — a confidently-held wrong model has to be dislodged, not merely topped up — so when you catch one, dig into its extent rather than moving on.
- **Map every strand the lesson rests on.** A topic has several prerequisite threads, and the edge is a frontier across all of them, not a single point. Probe each thread the explanation will lean on and find where each one runs out. Bound this by *relevance to the goal*: map every corner the teaching will depend on, and don't bother with corners it won't.

Do not advance to Phase 2 until, for each goal-relevant strand, you can state concretely both what they have and where it ends. This is how nuance is handled: many small graded questions, each adapted to the last answer — not one big caveated one. Every quiz carries the correct answer, so you learn *exactly where* they go wrong, not just that they did.

**1b. Their learning goal — use AskUserQuestion.** Find out what they actually want taught. With a subject they don't know yet, the goal is often hard to articulate — "I want to understand LLMs" or "how RAG works" can mean ten different things, and which one it is completely changes what you teach. Interrogate the vision until it's concrete. This has no right answer, so it's AskUserQuestion, never quiz. (When the session comes from a mentorship lesson or a curriculum lesson, the source already fixes most of the goal — confirm scope and depth, don't re-interrogate.)

### Phase 2 — Plan (think hard here)

This is the highest-leverage step; don't rush it. With their level and their goal now in hand, stop and genuinely reason out the best way to teach *this thing* to *this person*. Re-read the philosophy above and plan against it.

**Gather the sources first.** Every concept may be covered by more than one source, and each gives a different kind of depth:

- **Mentorship** (`Fontes/Mentoria/` in the vault) — *practice* depth: real problems, decisions, trade-offs, what breaks in production. Dense, with many assumed prerequisites and skipped steps. Grep the transcripts for the concept; cite passages you use.
- **Curriculum** (`curriculum/` in this project — the cloned `ai-engineering-from-scratch` repo; lesson text in `phases/<phase>/<lesson>/docs/en.md`, code in `code/`, questions in `quiz.json`) — *mechanism* depth: the math, the from-scratch code, why it works.
- **Vault** — what the learner already has: `Conceitos/` notes, previous lessons, their drawings.
- **`researcher` subagent** — fire a quick one to map the field: core concepts, the real first principles, standard framings, common gotchas, and to settle anything the sources disagree on or leave thin. Cheap, and it makes the whole plan more accurate.

Use them for different steps of the loop: the mentor's real problem is usually the best **Motivate**; the curriculum's mechanism is usually the best **Establish**; **Connect** uses both (the mechanism explains the mentor's practical decision). When sources disagree, that disagreement is content — surface it (the mentor may be simplifying on purpose, or practice may legitimately differ from the textbook).

Then plan:
- What are the unconditional truths this rests on? Is there a clean atomic unit ("ALL X is done through {____}")?
- Which of those do they already hold (from Phase 1a and the vault)? Build from there — not below it, not above it.
- What's the motivated discovery path from those truths to their goal? Where does each step come from — why would anyone reach for it?
- Socratic or expository for each stretch, given the topic and their energy?
- One concept per session. If the goal needs several big concepts, split into sessions and say so.

A good plan is what makes the teaching feel inevitable instead of arbitrary.

**Then present the plan — always, before any teaching** (in a study session: written into the lesson note and opened in Obsidian, with a short pointer in chat). Two parts:

1. **The approach, in prose.** What we'll cover, in what order, which sources feed which part, and why this way — given where their edge sits (Phase 1a) and what they're reaching for (Phase 1b). A few freeform sentences.
2. **The dependency map.** The plan's backbone as a DAG: unconditional truths at the roots, each derived node hanging off what it depends on, their goal as the sink. Draw it as a small ```mermaid``` graph (Obsidian renders it in the lesson note). This map *is* the teaching order — Phase 3 builds it node by node. Keep it small: few nodes, short labels — a map, not the territory.

**Stress-test the roots before presenting.** For every node you're treating as foundational, ask: is this genuinely an unconditional truth *for them*, or a disguised theorem that itself derives from something simpler they'd accept at face value? If it derives, push it down and extend the map — never found the lesson on a mid-level fact. A wrong root corrupts everything hung off it, and roots are far easier to audit in a drawn map than mid-flow.

**Then stop and wait for their go-ahead.** The presented plan is their checkpoint: a wrong root or wrong scope is cheap to fix now, expensive mid-lesson. Do not begin Phase 3 until they okay the plan.

### Phase 3 — Teach (the loop)

Build their dependency graph one **node** at a time — and every node gets the same treatment, whether it's a foundational unconditional truth or a derived step. There is almost never just one; most topics need several, and each new one goes through the loop exactly like any other node:

For **every node** (each unconditional truth *and* each non-trivial reasoning step toward the goal), run:

1. **Motivate.** Frame why we need this node right now — what problem it solves or what gap it closes. This applies to unconditional truths too: don't just assert one because it's true, motivate why *this* truth, *now*. "Why are we even bringing this in?"
2. **Establish.**
   - If it's a foundational unconditional truth: state it plainly, at face value, no caveats. Surface an atomic unit if one fits.
   - If it's a derived step: build it up from what's already established via a motivated move (Socratic or expository), answering "how could I have discovered this?" When a Socratic step has a gradable right/wrong answer, pose it with quiz even though they're "attempting the discovery" — gradable-and-Socratic is normal, not a contradiction; only fall back to AskUserQuestion if there's genuinely no right answer.
   - When teaching from a dense source (a mentor's passage), quote the passage, then unpack it: "O mentor disse X. Por que X? Vamos reconstruir…" — the learner should always see the link between the dense sentence and the opened-up explanation.
3. **Connect.** Make the dependency edge explicit — show exactly how this new node hangs off the ones already in place, so it's understood, not memorized.
4. **Quiz-check.** Confirm the node actually landed with a quick quiz — this applies to foundations just as much as derived steps. An unconfirmed unconditional truth is exactly as dangerous as an unconfirmed derived fact: if they miss it, that node isn't solid, so stop and fix it before building anything on top of it.

Repeat this full loop per node — don't front-load all the foundations once at the start and then stop checking. Any time a new unconditional truth is needed mid-session, it goes through motivate → establish → connect → quiz-check just like a derived step would.

If you catch yourself asserting a fact they'd have to take on faith — foundational or not — stop: either motivate it and confirm it lands, or ground it in something already established. Unmotivated, unconfirmed facts don't lock in — that's the whole point.

### Phase 4 — Consolidate into the vault

At the end of a study session (or whenever the learner asks), write what was built into `~/Documents/AI Engineering/`. Before writing, read the note if it exists — **add to it, never overwrite or delete what the learner wrote**.

1. **Lesson note** in `Aulas/<Mentoria|Currículo|Livre>/…` — in a study session it already holds the plan and the nodes (the whiteboard above); tidy it rather than rewrite. It follows `Templates/Aula.md`: objective, sources, starting point (what Phase 1 found), the dependency map, the unfolded explanation node by node with `[[links]]` to concepts, quiz score and the misses worth remembering, next steps. Write it as a clean, rereadable explanation — not a chat transcript.
2. **Concept notes** in `Conceitos/`, one per node taught, following `Templates/Conceito.md`. Fill `Depende de::` / `Usado em::` with `[[links]]` (these are the graph's edges — keep them true), the unconditional truth or definition, the discovery path, and source citations (`fontes:` in the frontmatter). Put mechanism content under *Mecanismo* and practical content under *Na prática*. Add misses from `.claude/state/quiz-log.jsonl` (same `topic`) under *Erros que eu cometi*.
3. **Status**: `aprendendo` after the first session; `sólido` only when the node passed its quiz-check cleanly *and* held up later (a later probe, or a correct drawing); `revisar` when a later probe or drawing shows it slipped.
4. **`00 Mapa.md`**: update the trail tables, the concepts-by-status lists, and the deepening queue (concepts that came up but still need their own session).
5. **Close** by suggesting `/desenho` for the session's main idea — drawing it from memory is the learner's own consolidation step (`/revisar-desenho` checks it).

Diagrams in lessons and notes follow the `visualize` skill.

Concept note names: the concept's usual name, in the form the learner will search for (English technical terms stay English: `Self-attention.md`, `Re-ranking.md`; Portuguese for general ideas: `Produto escalar.md`). Check `Conceitos/` for an existing note (including near-duplicates) before creating one.

## Formatting — math renders as LaTeX

Everything written for the learner ends up in Obsidian, which renders LaTeX natively. So whenever math notation is involved — explanations, questions, quiz options and explanations, notes, anything — write it in LaTeX instead of plain-text approximations:

- Inline math: `$f(x)$`
- Centered display math: `$$` fenced on its own lines, e.g. `$$\n f(x) \n$$`

If LaTeX can be used, it should be. Write $f(x) = x^2$, not `f(x) = x^2`.

**Exception — the terminal (learner's request, 2026-10-06):** the quiz popup and chat replies don't render LaTeX. There, write math in **Unicode** — `f(x) = x²`, `√dₖ`, `Σᵢ wᵢ·xᵢ`, `∇L`, `η`, `≈`, `≤`, `→`, `θ` — never `$…$` source. LaTeX stays for everything written to the vault.
