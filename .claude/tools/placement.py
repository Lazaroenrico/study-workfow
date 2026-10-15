#!/usr/bin/env python3
"""Helper data for /nivelamento: career routes, placement strands, lesson quiz availability.

    python3 .claude/tools/placement.py routes                       # career routes to choose from
    python3 .claude/tools/placement.py strands [--route <id>]       # strands, lessons, quiz stock, route relevance
    python3 .claude/tools/placement.py route-lessons <id>           # a route's lessons, in order, with minutes
    python3 .claude/tools/placement.py check                        # validate strands.json against the clone

Never prints quiz answers. Lesson ids are '<phase-dir>/<lesson-dir>' under curriculum/phases/.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURRICULUM = ROOT / "curriculum"
PHASES = CURRICULUM / "phases"
STRANDS = Path(__file__).resolve().parent / "strands.json"


def load_strands() -> list[dict]:
    return json.loads(STRANDS.read_text(encoding="utf-8"))["strands"]


def routes() -> list[dict]:
    out = []
    for f in sorted((CURRICULUM / "learning-paths").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("lessons"):
            out.append(d)
    return out


def route_lessons(route: dict) -> list[dict]:
    return [l for l in route.get("lessons", []) if isinstance(l, dict) and l.get("path")]


def lesson_id(path: str) -> str:
    return path.removeprefix("phases/")


def quiz_stock(lid: str) -> str:
    qf = PHASES / lid / "quiz.json"
    if not qf.is_file():
        return "sem quiz"
    counts: dict[str, int] = {}
    data = json.loads(qf.read_text(encoding="utf-8"))
    for q in data.get("questions", []) if isinstance(data, dict) else data:
        counts[q.get("stage", "?")] = counts.get(q.get("stage", "?"), 0) + 1
    return " ".join(f"{k}:{v}" for k, v in counts.items()) or "sem quiz"


def phase_minutes_per_lesson() -> dict[str, int]:
    """Average minutes per lesson, from ROADMAP.md phase hours / lessons in the phase."""
    roadmap = (CURRICULUM / "ROADMAP.md").read_text(encoding="utf-8")
    hours = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"^## Phase (\d+):.*\(~(\d+(?:\.\d+)?) hours\)", roadmap, re.M)}
    out = {}
    for d in PHASES.iterdir():
        if d.is_dir() and d.name[:2].isdigit():
            n = sum(1 for x in d.iterdir() if x.is_dir())
            if n and int(d.name[:2]) in hours:
                out[d.name] = round(hours[int(d.name[:2])] * 60 / n)
    return out


def title_of(lid: str) -> str:
    doc = PHASES / lid / "docs" / "en.md"
    if doc.is_file():
        for line in doc.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return lid.split("/")[-1]


def cmd_routes() -> int:
    for r in routes():
        mins = r.get("estimatedMinutes") or sum(l.get("minutes", 0) for l in route_lessons(r))
        kind = "carreira" if r.get("kind") == "career-route" else "trilha"
        print(f"- {r['id']} [{kind}] — {r['title']} (~{round(mins / 60)} h, {len(route_lessons(r))} aulas)")
        if r.get("decisionPrompt"):
            print(f"    pergunta: {r['decisionPrompt']}")
        print(f"    {r.get('summary', '')}")
        cov = r.get("coverage") or {}
        if cov.get("outsideCourse"):
            print(f"    fora do curso: {'; '.join(cov['outsideCourse'])}")
        if r.get("baseline"):
            print(f"    pré-requisito: {' '.join(r['baseline'])}")
    return 0


def cmd_route_lessons(rid: str) -> int:
    r = next((r for r in routes() if r["id"] == rid), None)
    if not r:
        print(f"unknown route: {rid}")
        return 2
    for l in route_lessons(r):
        lid = lesson_id(l["path"])
        req = "obrigatória" if l.get("required", True) else "opcional"
        print(f"{l.get('order', '?'):>2}. {lid} — {title_of(lid)} ({l.get('minutes', '?')} min, {req}, quiz: {quiz_stock(lid)})")
    return 0


def cmd_strands(rid: str | None) -> int:
    in_route: set[str] = set()
    if rid:
        r = next((r for r in routes() if r["id"] == rid), None)
        if not r:
            print(f"unknown route: {rid}")
            return 2
        in_route = {lesson_id(l["path"]) for l in route_lessons(r)}
    per_lesson = phase_minutes_per_lesson()
    strands = load_strands()
    touched = {s["id"] for s in strands if in_route & set(s["lessons"])}
    # a strand the route touches makes its dependencies relevant too
    needed, stack = set(touched), list(touched)
    by_id = {s["id"]: s for s in strands}
    while stack:
        for dep in by_id[stack.pop()]["deps"]:
            if dep not in needed:
                needed.add(dep)
                stack.append(dep)
    for s in strands:
        if rid:
            rel = "ROTA" if s["id"] in touched else ("BASE da rota" if s["id"] in needed else "fora da rota")
        else:
            rel = ""
        mins = sum(per_lesson.get(l.split("/")[0], 0) for l in s["lessons"])
        print(f"\n## {s['id']} — {s['title']}  [{s['layer']}] {rel}".rstrip())
        print(f"deps: {', '.join(s['deps']) or '—'} · ~{round(mins / 60)} h · palavras-chave: {', '.join(s['keywords'])}")
        for i, lid in enumerate(s["lessons"]):
            mark = " *" if lid in in_route else ""
            print(f"  [{i}] {lid} — {title_of(lid)} (quiz: {quiz_stock(lid)}){mark}")
    if rid:
        print("\n(* = aula da rota)")
    return 0


def cmd_check() -> int:
    bad = 0
    seen: set[str] = set()
    ids = {s["id"] for s in load_strands()}
    for s in load_strands():
        for dep in s["deps"]:
            if dep not in ids:
                print(f"{s['id']}: unknown dep {dep}")
                bad += 1
        for lid in s["lessons"]:
            if not (PHASES / lid / "docs" / "en.md").is_file():
                print(f"{s['id']}: missing lesson {lid}")
                bad += 1
            seen.add(lid)
    for r in routes():
        for l in route_lessons(r):
            if not (CURRICULUM / l["path"]).is_dir():
                print(f"route {r['id']}: missing lesson {l['path']}")
                bad += 1
    print(f"{len(load_strands())} strands, {len(seen)} lessons, {len(routes())} routes — {'OK' if not bad else f'{bad} problems'}")
    return 1 if bad else 0


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args[0] == "routes":
        return cmd_routes()
    if args[0] == "route-lessons" and len(args) > 1:
        return cmd_route_lessons(args[1])
    if args[0] == "strands":
        return cmd_strands(args[2] if len(args) > 2 and args[1] == "--route" else None)
    if args[0] == "check":
        return cmd_check()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
