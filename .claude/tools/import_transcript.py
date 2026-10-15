#!/usr/bin/env python3
"""Import a plain-text mentorship transcript into the vault, intact, with citable paragraphs.

    python3 .claude/tools/import_transcript.py <transcript.txt> --title "RAG avançado" [--date 2026-10-05] [--force]
    python3 .claude/tools/import_transcript.py <file> --prefix S02 --title "Pré-aula LangChain" --modulo "S02 LangChain e LangGraph" [--tipo pre-aula] [--markdown]

Writes `Fontes/Mentoria/<prefix or date> <title>.md`. The text itself is never edited: it is only
split into paragraphs, each ending in an Obsidian block id (`^p1`, `^p2`, …) so notes can
cite an exact passage with `[[<date> <title>#^p12]]`.

--markdown keeps an already-structured note (a summary with headings and bullets) line by
line, adding a block id to every non-heading line instead of re-flowing it.

Paragraphs: blank-line separated blocks when the transcript has them; otherwise (one wall
of text, or one caption per line) the text is re-flowed into ~700-character chunks on
sentence boundaries, falling back to ~120-word chunks when there is no punctuation.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

VAULT = Path.home() / "Documents" / "AI Engineering"
DEST = VAULT / "Fontes" / "Mentoria"
TARGET_CHARS = 700
MAX_CHARS = 1500
LONG_LESSON_WORDS = 6000  # ~45 min of speech


def read_text(path: Path) -> str:
    data = path.read_bytes()
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            text = data.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    return text.replace("\r\n", "\n").replace("\r", "\n")


def chunk(text: str) -> list[str]:
    """Split one long run of text into ~TARGET_CHARS pieces without changing any word."""
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    sentences = re.split(r"(?<=[.!?…])\s+", text)
    if len(sentences) == 1 and len(text) > MAX_CHARS:
        words = text.split(" ")
        return [" ".join(words[i:i + 120]) for i in range(0, len(words), 120)]
    out, cur = [], ""
    for s in sentences:
        if cur and len(cur) + 1 + len(s) > TARGET_CHARS:
            out.append(cur)
            cur = s
        else:
            cur = f"{cur} {s}" if cur else s
    if cur:
        out.append(cur)
    # a single sentence can still be huge (no punctuation for a long stretch)
    final = []
    for p in out:
        if len(p) > MAX_CHARS * 2:
            words = p.split(" ")
            final += [" ".join(words[i:i + 120]) for i in range(0, len(words), 120)]
        else:
            final.append(p)
    return final


def paragraphs(text: str) -> list[str]:
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    if len(blocks) <= 1:
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        avg = sum(map(len, lines)) / max(1, len(lines))
        # long lines = one paragraph per line; short lines = captions, re-flow them
        blocks = lines if avg >= 200 else [" ".join(lines)]
    out: list[str] = []
    for b in blocks:
        flat = re.sub(r"\s*\n\s*", " ", b)
        out += chunk(flat) if len(flat) > MAX_CHARS else [flat]
    return out


def markdown_blocks(text: str) -> tuple[str, int]:
    """Keep the note as is; append ^pN to each non-empty, non-heading line."""
    out, n = [], 0
    for line in text.split("\n"):
        if line.strip() and not line.lstrip().startswith("#"):
            n += 1
            out.append(f"{line.rstrip()} ^p{n}")
        else:
            out.append(line.rstrip())
    return "\n".join(out).strip(), n


def safe_title(title: str) -> str:
    return re.sub(r'[\\/:*?"<>|#^\[\]]', "-", title).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path)
    ap.add_argument("--title", required=True)
    ap.add_argument("--date", help="lesson date, YYYY-MM-DD (default: today, unless --prefix is given)")
    ap.add_argument("--prefix", help="name prefix instead of the date, e.g. S02 for week 2")
    ap.add_argument("--modulo", help="module (overview folder) this source belongs to; default: the note itself")
    ap.add_argument("--tipo", default="aula", help="pre-aula | aula | resumo | …")
    ap.add_argument("--markdown", action="store_true", help="source is a structured markdown note: keep its lines")
    ap.add_argument("--force", action="store_true", help="overwrite an existing source note")
    args = ap.parse_args()

    if not args.source.is_file():
        print(f"Source not found: {args.source}")
        return 2
    if args.date:
        try:
            datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("--date must be YYYY-MM-DD")
            return 2
    elif not args.prefix:
        args.date = date.today().isoformat()

    raw = read_text(args.source)
    if args.markdown:
        body, count = markdown_blocks(raw)
        words = len(raw.split())
    else:
        paras = paragraphs(raw)
        body, count = "\n\n".join(f"{p} ^p{i}" for i, p in enumerate(paras, 1)), len(paras)
        words = sum(len(p.split()) for p in paras)
    if not count:
        print("Transcript is empty.")
        return 2
    name = f"{args.prefix or args.date} {safe_title(args.title)}"
    target = DEST / f"{name}.md"
    if target.exists() and not args.force:
        print(f"Already imported: {target}\n(use --force to overwrite)")
        return 3

    modulo = safe_title(args.modulo) if args.modulo else name
    note = (
        "---\n"
        "tags: [fonte, mentoria]\n"
        f"titulo: \"{args.title}\"\n"
        + (f"data: {args.date}\n" if args.date else "")
        + (f"semana: {args.prefix}\n" if args.prefix else "")
        + f"tipo: {args.tipo}\n"
        f"modulo: \"[[Aulas/Mentoria/{modulo}/00 Visão geral|{modulo}]]\"\n"
        f"importado: {date.today().isoformat()}\n"
        f"origem: \"{args.source.name}\"\n"
        f"paragrafos: {count}\n"
        f"palavras: {words}\n"
        "---\n"
        f"# {args.title}\n\n"
        f"> [!info] Transcript bruto da mentoria, sem edição. Cite trechos com `[[{name}#^p12]]`.\n"
        f"> Aula explicada: [[Aulas/Mentoria/{modulo}/00 Visão geral|{modulo}]]\n\n"
        f"{body}\n"
    )
    DEST.mkdir(parents=True, exist_ok=True)
    target.write_text(note, encoding="utf-8")
    kind = "longa" if words > LONG_LESSON_WORDS else "curta"
    print(f"Imported: {target}\nNote name: {name}\nParagraphs: {count} (^p1–^p{count})\n"
          f"Words: {words} (~{round(words / 140)} min de fala) — aula {kind}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
