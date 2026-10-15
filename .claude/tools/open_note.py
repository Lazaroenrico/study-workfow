#!/usr/bin/env python3
"""Open a vault note in Obsidian (the teaching "whiteboard").

    python3 .claude/tools/open_note.py "Aulas/Currículo/13-tools-and-protocols/01-the-tool-interface.md"

The path is relative to the vault (or absolute inside it). Obsidian reloads an open note when
the file changes, so the teacher can keep appending to it and the learner sees it live.
"""

from __future__ import annotations

import subprocess
import sys
import urllib.parse
from pathlib import Path

VAULT = Path.home() / "Documents" / "AI Engineering"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    note = Path(sys.argv[1]).expanduser()
    if not note.is_absolute():
        note = VAULT / note
    try:
        rel = note.resolve().relative_to(VAULT.resolve()).as_posix().removesuffix(".md")
    except ValueError:
        print(f"Not inside the vault: {note}", file=sys.stderr)
        return 2
    if not note.exists():
        print(f"Note does not exist yet: {note}", file=sys.stderr)
        return 1
    uri = "obsidian://open?" + urllib.parse.urlencode({"vault": VAULT.name, "file": rel}, quote_via=urllib.parse.quote)
    subprocess.Popen(["xdg-open", uri], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    print(f"Opened in Obsidian: {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
