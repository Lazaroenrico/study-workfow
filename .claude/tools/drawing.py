#!/usr/bin/env python3
"""Excalidraw drawings for retrieval practice, in the vault's Desenhos/ folder.

    python3 .claude/tools/drawing.py new --title "Self-attention" --prompt "Desenhe, de memória, …" \
        [--aula "Aulas/Currículo/07-transformers-deep-dive/02-self-attention-from-scratch"] \
        [--conceito "Self-attention" --conceito "Softmax"] [--no-open]
    python3 .claude/tools/drawing.py find [name-or-substring]

`new` writes `Desenhos/<slug>-<date>.excalidraw.md` — an Obsidian Excalidraw drawing that
holds only the title and the prompt (locked, top-left) — and opens it in Obsidian.
`find` prints the drawing (latest, or the one matching) with its exported PNG, if any, and
its typed text elements. The PNG exists when the Excalidraw plugin's "Auto-export PNG"
setting is on (or after a manual export to the vault).
"""

from __future__ import annotations

import argparse
import json
import random
import re
import subprocess
import sys
import time
import unicodedata
import urllib.parse
from datetime import date
from pathlib import Path

VAULT = Path.home() / "Documents" / "AI Engineering"
DRAWINGS = VAULT / "Desenhos"

HEADER = (
    "==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== "
    "You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. "
    "For more info check in plugin settings under 'Saving'"
)


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "desenho"


def text_element(eid: str, text: str, x: int, y: int, size: int, color: str) -> dict:
    lines = text.split("\n")
    width = max(len(l) for l in lines) * size * 0.55
    height = len(lines) * size * 1.25
    return {
        "id": eid, "type": "text", "x": x, "y": y, "width": round(width, 1), "height": round(height, 1),
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent", "fillStyle": "solid",
        "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [],
        "frameId": None, "roundness": None, "seed": random.randint(1, 2**31 - 1), "version": 1,
        "versionNonce": random.randint(1, 2**31 - 1), "isDeleted": False, "boundElements": None,
        "updated": int(time.time() * 1000), "link": None, "locked": True,
        "text": text, "rawText": text, "originalText": text, "fontSize": size, "fontFamily": 1,
        "textAlign": "left", "verticalAlign": "top", "containerId": None, "autoResize": True,
        "lineHeight": 1.25,
    }


def wrap(text: str, width: int = 70) -> str:
    out, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > width:
            out.append(line)
            line = word
        else:
            line = f"{line} {word}" if line else word
    return "\n".join(out + [line])


def build_note(title: str, prompt: str, aula: str | None, conceitos: list[str]) -> str:
    prompt = wrap(prompt)
    title_id, prompt_id = "titulo01", "enunciado01"
    scene = {
        "type": "excalidraw", "version": 2, "source": "learn-system",
        "elements": [
            text_element(title_id, title, 0, 0, 28, "#1e1e1e"),
            text_element(prompt_id, prompt, 0, 50, 18, "#868e96"),
        ],
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }
    fm = ["---", "", "excalidraw-plugin: parsed", "tags: [excalidraw, desenho]", f"criado: {date.today().isoformat()}"]
    if aula:
        fm.append(f'aula: "[[{aula}]]"')
    if conceitos:
        fm.append("conceitos: [" + ", ".join(f'"[[{c}]]"' for c in conceitos) + "]")
    fm += ["revisado: false", "", "---"]
    return "\n".join(fm) + f"""
{HEADER}


# Excalidraw Data

## Text Elements
{title} ^{title_id}

{prompt} ^{prompt_id}

%%
## Drawing
```json
{json.dumps(scene, ensure_ascii=False, indent="\t")}
```
%%"""


def open_in_obsidian(note: Path) -> None:
    rel = note.relative_to(VAULT).as_posix().removesuffix(".md")
    uri = "obsidian://open?" + urllib.parse.urlencode({"vault": VAULT.name, "file": rel}, quote_via=urllib.parse.quote)
    subprocess.Popen(["xdg-open", uri], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)


def cmd_new(args) -> int:
    DRAWINGS.mkdir(parents=True, exist_ok=True)
    base = f"{slugify(args.title)}-{date.today().isoformat()}"
    note = DRAWINGS / f"{base}.excalidraw.md"
    n = 2
    while note.exists():
        note = DRAWINGS / f"{base}-{n}.excalidraw.md"
        n += 1
    note.write_text(build_note(args.title, args.prompt, args.aula, args.conceito or []), encoding="utf-8")
    if not args.no_open:
        open_in_obsidian(note)
    embed = note.name.removesuffix(".md")
    print(f"Created: {note}\nEmbed: ![[{embed}|600]]" + ("" if args.no_open else "\nOpened in Obsidian."))
    return 0


def png_for(note: Path) -> Path | None:
    """The auto-exported PNG. With "export both light and dark" on, the plugin writes
    x.excalidraw.light.png / x.excalidraw.dark.png; prefer light (dark strokes on white)."""
    stem = note.name.removesuffix(".md")  # x.excalidraw
    bare = stem.removesuffix(".excalidraw")
    for name in (f"{stem}.light.png", f"{stem}.png", f"{bare}.light.png", f"{bare}.png", f"{stem}.dark.png"):
        cand = note.with_name(name)
        if cand.exists():
            return cand
    return None


def cmd_find(args) -> int:
    notes = sorted(DRAWINGS.glob("*.excalidraw.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if args.name:
        notes = [p for p in notes if args.name.lower() in p.name.lower()]
    if not notes:
        print("No drawing found.")
        return 1
    note = notes[0]
    text = note.read_text(encoding="utf-8")
    png = png_for(note)
    print(f"Drawing: {note}")
    if png:
        fresh = png.stat().st_mtime >= note.stat().st_mtime - 5
        print(f"PNG: {png}" + ("" if fresh else "  (older than the drawing — may be stale; re-export)"))
    else:
        print("PNG: none — enable Excalidraw › Embedding & export › Auto-export PNG, or export the drawing to the vault")
    fm = re.search(r"^---\n(.*?)\n---", text, re.S)
    if fm:
        print("Frontmatter:\n" + "\n".join("  " + l for l in fm.group(1).strip().splitlines()))
    te = re.search(r"## Text Elements\n(.*?)(?:\n%%|\n## )", text, re.S)
    if te:
        typed = re.sub(r" \^[\w-]+$", "", te.group(1).strip(), flags=re.M)
        print("Typed text elements:\n" + "\n".join("  " + l for l in typed.splitlines()))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new")
    n.add_argument("--title", required=True)
    n.add_argument("--prompt", required=True)
    n.add_argument("--aula", help="vault path of the lesson note, without .md")
    n.add_argument("--conceito", action="append", help="concept note name (repeatable)")
    n.add_argument("--no-open", action="store_true")
    f = sub.add_parser("find")
    f.add_argument("name", nargs="?")
    args = ap.parse_args()
    return cmd_new(args) if args.cmd == "new" else cmd_find(args)


if __name__ == "__main__":
    sys.exit(main())
