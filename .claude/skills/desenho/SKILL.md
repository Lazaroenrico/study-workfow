---
name: desenho
description: Start a from-memory drawing (retrieval practice) in Excalidraw in the vault — creates a drawing with only a title and a prompt, linked to the lesson and concepts, and opens it in Obsidian for the learner to draw with their tablet. Use at the end of a study session, or for /desenho, "quero desenhar", "vou consolidar desenhando".
argument-hint: "[tema]"
---

# Desenho — consolidate by drawing from memory

Drawing a lesson's idea **from memory** is retrieval practice: it shows whether the dependency graph actually landed. The learner draws by hand (tablet) in Excalidraw inside Obsidian; afterwards `/revisar-desenho` checks it.

**Never show the reference before they draw** — no diagram, no map, no summary in chat while they're drawing. Seeing it first turns retrieval into copying.

## Steps

1. **Pick the idea** (argument: `$ARGUMENTS`). Default: the main idea of the session that just ended. It should be one idea with structure — something that is a picture (a flow, a dependency, a mechanism, a geometry), the core of the lesson's map. If unclear, ask with AskUserQuestion.
2. **Write the prompt** in Portuguese: one or two sentences that ask for the structure, not the words. Name what must appear without giving it away.
   - Good: *"Desenhe, de memória, o caminho de um token pela self-attention: de onde saem Q, K e V, o que é comparado com o quê, e como sai o vetor final."*
   - Bad: *"Desenhe Q·Kᵀ → softmax → ×V"* (that's the answer).
3. **Create and open it:**
   ```bash
   python3 .claude/tools/drawing.py new --title "<tema>" --prompt "<enunciado>" \
     --aula "<caminho da nota da aula no vault, sem .md>" --conceito "<Conceito>" [--conceito ...]
   ```
   It creates `Desenhos/<slug>-<data>.excalidraw.md` and opens it in Obsidian.
4. **Link it**: embed the drawing (the `Embed:` line printed) under *Desenho* in the lesson note, and under *Desenhos* in each concept note.
5. Tell the learner, briefly: draw with the pen, take as long as needed, and run `/revisar-desenho` when done. Nothing else.

## If the drawing doesn't open in Excalidraw

The vault needs the **Excalidraw** community plugin (Obsidian › Configurações › Plugins da comunidade › Excalidraw, by Zsolt Viczian), with *Embedding & export › Auto-export PNG* turned on so `/revisar-desenho` can see the drawing. If the file opens as markdown text, the plugin isn't installed or enabled.
