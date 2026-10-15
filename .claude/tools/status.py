#!/usr/bin/env python3
"""Snapshot of the study system's state, for /manual (and for "o que faço agora?").

    python3 .claude/tools/status.py

Reads the vault, LEARNING.md, the quiz log and the md-log links. Read-only.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VAULT = Path.home() / "Documents" / "AI Engineering"
STATE = ROOT / ".claude" / "state"


def frontmatter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def section(title: str) -> None:
    print(f"\n## {title}")


def main() -> None:
    print(f"# Estado do sistema — {datetime.now():%Y-%m-%d %H:%M}")

    section("Instalação")
    checks = [
        ("vault", VAULT.is_dir()),
        ("currículo clonado", (ROOT / "curriculum" / "phases").is_dir()),
        ("plugin Excalidraw", (VAULT / ".obsidian/plugins/obsidian-excalidraw-plugin").is_dir()),
        ("mermaid-cli (diagramas)", (ROOT / ".claude/tools/node_modules/.bin/mmdc").exists()),
    ]
    excalidraw = VAULT / ".obsidian/plugins/obsidian-excalidraw-plugin/data.json"
    if excalidraw.is_file():
        d = json.loads(excalidraw.read_text(encoding="utf-8"))
        checks.append(("Excalidraw auto-export PNG", bool(d.get("autoexportPNG"))))
        checks.append(("Excalidraw folder = Desenhos", d.get("folder") == "Desenhos"))
    for name, ok in checks:
        print(f"- {'✓' if ok else '✗'} {name}")

    section("Conceitos (vault)")
    concepts = sorted((VAULT / "Conceitos").glob("*.md"))
    by_status = Counter(frontmatter(c).get("status", "?") for c in concepts)
    print(f"- {len(concepts)} conceitos: " + (", ".join(f"{k}: {v}" for k, v in by_status.items()) or "nenhum ainda"))
    revisar = [c.stem for c in concepts if frontmatter(c).get("status") == "revisar"]
    if revisar:
        print(f"- para revisar: {', '.join(revisar[:10])}")

    section("Mentoria")
    lessons = sorted((VAULT / "Aulas/Mentoria").glob("*/00 Visão geral.md"))
    sources = sorted((VAULT / "Fontes/Mentoria").glob("*.md"))
    print(f"- {len(sources)} transcripts importados, {len(lessons)} aulas analisadas")
    for ov in lessons:
        text = ov.read_text(encoding="utf-8")
        pending = len(re.findall(r"^\|.*\|\s*(pendente|em andamento)\s*\|\s*$", text, re.M))
        st = frontmatter(ov).get("status", "?")
        print(f"  - {ov.parent.name}: {st}" + (f", {pending} bloco(s) pendente(s)" if pending else ""))

    section("Currículo")
    learning = ROOT / "LEARNING.md"
    if not learning.is_file():
        print("- sem LEARNING.md — nivelamento ainda não feito (/nivelamento)")
    else:
        text = learning.read_text(encoding="utf-8")
        done = len(re.findall(r"^- \[x\]", text, re.M | re.I))
        todo = re.findall(r"^- \[ \] (.+)$", text, re.M)
        print(f"- fila de estudo: {done} feitas, {len(todo)} pendentes")
        if todo:
            print(f"- próxima: {todo[0]}")
        review = re.search(r"## Review queue\n(.*?)(?:\n## |\Z)", text, re.S)
        items = [l for l in (review.group(1).splitlines() if review else []) if l.strip().startswith(("-", "|")) and "---" not in l]
        if items:
            print(f"- review queue: {len(items)} item(s)")
    placement = sorted((VAULT / "Aulas").glob("Nivelamento *.md"))
    if placement and frontmatter(placement[-1]).get("status") == "em andamento":
        print(f"- nivelamento em andamento: {placement[-1].name} (/nivelamento continuar)")

    section("Quizzes")
    log = STATE / "quiz-log.jsonl"
    entries = []
    if log.is_file():
        for line in log.read_text(encoding="utf-8").splitlines():
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    answered = [e for e in entries if e.get("status") == "answered"]
    if not answered:
        print("- nenhum quiz respondido ainda")
    else:
        right = sum(1 for e in answered if e.get("isCorrect"))
        dk = sum(1 for e in answered if e.get("dontKnow"))
        print(f"- {len(answered)} respondidos: {right} certos, {len(answered) - right - dk} errados, {dk} 'não sei'")
        misses = [e for e in answered[-30:] if not e.get("isCorrect")]
        topics = Counter(e.get("topic") or "?" for e in misses)
        if topics:
            print("- erros recentes por tema: " + ", ".join(f"{t} ({n})" for t, n in topics.most_common(6)))

    section("Desenhos")
    drawings = sorted((VAULT / "Desenhos").glob("*.excalidraw.md"))
    unreviewed = [d.name.removesuffix(".excalidraw.md") for d in drawings if frontmatter(d).get("revisado") == "false"]
    print(f"- {len(drawings)} desenhos, {len(unreviewed)} sem revisão" + (f": {', '.join(unreviewed[:5])}" if unreviewed else ""))

    section("Sessões")
    sessions = sorted((VAULT / "Sessões").glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    print(f"- {len(sessions)} sessões registradas" + (f"; última: {sessions[0].stem}" if sessions else ""))

    mapa = VAULT / "00 Mapa.md"
    if mapa.is_file():
        queue = re.search(r"## Fila de aprofundamento\n(.*?)(?:\n## |\Z)", mapa.read_text(encoding="utf-8"), re.S)
        items = [l.strip() for l in (queue.group(1).splitlines() if queue else []) if re.match(r"\s*- \[ \] \S", l)]
        section("Fila de aprofundamento (00 Mapa)")
        print(f"- {len(items)} item(s)" + ("".join(f"\n  {i}" for i in items[:5]) if items else ""))


if __name__ == "__main__":
    main()
