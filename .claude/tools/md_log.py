#!/usr/bin/env python3
"""md-log — mirror the study session into a markdown note in the vault (port of learn's md-log).

    python3 .claude/tools/md_log.py link ["Sessões/2026-10-05 RAG.md"]   # link a note (default: Sessões/<now>.md)
    python3 .claude/tools/md_log.py off                                   # stop logging
    python3 .claude/tools/md_log.py status
    python3 .claude/tools/md_log.py hook      # called by the Stop / PostToolUse hooks (JSON on stdin)

The linked note is regenerated from the Claude Code transcript on every hook call, so it
is always complete (backfill is free) and in order. Captured: the learner's prompts, the
assistant's text, quiz questions with their graded answers, and AskUserQuestion Q&A.
Everything else (other tool calls, subagents, system messages) is left out.

Links are per session (CLAUDE_CODE_SESSION_ID), so several Claude Code sessions can log
to different notes at the same time. If the session id isn't available, the link binds to
the first session whose hook fires after `link`.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

VAULT = Path.home() / "Documents" / "AI Engineering"
STATE = Path(__file__).resolve().parent.parent / "state" / "md-log.json"
PASTE_LIMIT = 1500


# ── state ────────────────────────────────────────────────────────────────────


def load_state() -> dict:
    """{"sessions": {session_id: note path}, "pending": note path | None}"""
    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
        if isinstance(state.get("sessions"), dict):
            return state
    except (OSError, json.JSONDecodeError, AttributeError):
        pass
    return {"sessions": {}, "pending": None}


def save_state(state: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def current_session() -> str | None:
    return os.environ.get("CLAUDE_CODE_SESSION_ID") or None


def resolve_note(arg: str | None) -> Path:
    if not arg:
        arg = f"Sessões/{datetime.now():%Y-%m-%d %H%M}.md"
    p = Path(arg).expanduser()
    if not p.is_absolute():
        p = VAULT / p
    if p.suffix != ".md":
        p = p.with_name(p.name + ".md")
    return p


# ── transcript → items ───────────────────────────────────────────────────────

COMMAND_RE = re.compile(r"<command-name>/?([^<]+)</command-name>")
ARGS_RE = re.compile(r"<command-args>(.*?)</command-args>", re.S)
REMINDER_RE = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
PASTE_RE = re.compile(r"<pasted_content[^>]*>(.*?)</pasted_content[^>]*>", re.S)
HEREDOC_RE = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n(.*?)\n\1\s*$", re.S | re.M)


def clean_user_text(text: str) -> str | None:
    """Return the human-visible prompt, or None for non-human/meta messages."""
    m = COMMAND_RE.search(text)
    if m:
        args = ARGS_RE.search(text)
        return f"/{m.group(1).strip()} {args.group(1).strip() if args else ''}".strip()
    if text.lstrip().startswith(("<local-command", "<command-", "<bash-", "<task-notification")):
        return None
    if text.startswith("[Request interrupted"):
        return None
    text = REMINDER_RE.sub("", text)

    def paste(m):
        body = m.group(1).strip()
        if len(body) > PASTE_LIMIT:
            body = body[:PASTE_LIMIT].rstrip() + f" … _(+{len(m.group(1)) - PASTE_LIMIT} caracteres)_"
        return f"\n> [!quote]- Conteúdo colado\n> " + body.replace("\n", "\n> ") + "\n"

    text = PASTE_RE.sub(paste, text).strip()
    return text or None


def is_quiz_call(block: dict) -> bool:
    return block.get("name") == "Bash" and "quiz.py" in str((block.get("input") or {}).get("command", ""))


def tool_result_text(block: dict) -> str:
    c = block.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
    return ""


def parse_transcript(path: Path) -> tuple[list[tuple], dict, str | None]:
    """Return (items, results by tool_use_id, first timestamp)."""
    items: list[tuple] = []
    results: dict[str, str] = {}
    first_ts = None
    seen: set[str] = set()
    with path.open(encoding="utf-8") as f:
        for line in f:
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if e.get("type") not in ("user", "assistant") or e.get("isSidechain") or e.get("isMeta"):
                continue
            if e.get("uuid") in seen:
                continue
            seen.add(e.get("uuid"))
            first_ts = first_ts or e.get("timestamp")
            content = (e.get("message") or {}).get("content")
            blocks = [{"type": "text", "text": content}] if isinstance(content, str) else (content or [])
            for b in blocks:
                if not isinstance(b, dict):
                    continue
                kind = b.get("type")
                if e["type"] == "user":
                    if kind == "tool_result":
                        results[b.get("tool_use_id", "")] = tool_result_text(b)
                    elif kind == "text":
                        text = clean_user_text(b.get("text", ""))
                        if text and items[-1:] != [("user", text)]:  # resubmitted prompt
                            items.append(("user", text))
                else:
                    if kind == "text" and b.get("text", "").strip():
                        if items and items[-1][0] == "assistant":
                            items[-1] = ("assistant", items[-1][1] + "\n\n" + b["text"].strip())
                        else:
                            items.append(("assistant", b["text"].strip()))
                    elif kind == "tool_use" and is_quiz_call(b):
                        items.append(("quiz", b))
                    elif kind == "tool_use" and b.get("name") == "AskUserQuestion":
                        items.append(("ask", b))
    return items, results, first_ts


# ── rendering ────────────────────────────────────────────────────────────────


def quote(text: str) -> str:
    return "\n".join("> " + l if l else ">" for l in text.splitlines())


def strip_index(s: str) -> str:
    return re.sub(r"(^|, )\d+\. ", r"\1", s.strip())


def render_quiz(call: dict, result: str | None) -> str:
    cmd = str(call["input"].get("command", ""))
    spec = {}
    m = HEREDOC_RE.search(cmd)
    if m:
        try:
            spec = json.loads(m.group(2))
        except json.JSONDecodeError:
            spec = {}
    fields: dict[str, str] = {}
    if result:
        key = None
        for line in result.splitlines():
            m2 = re.match(r"(Question|Selected|Correct|User's note|Explanation): ?(.*)", line)
            if m2:
                key = m2.group(1)
                fields[key] = m2.group(2)
            elif key == "Explanation":
                fields[key] += "\n" + line
    question = spec.get("question") or fields.get("Question") or "(pergunta)"
    topic = spec.get("topic")
    lines = [f"> [!question] Quiz{' · ' + topic if topic else ''}", quote(question)]
    if spec.get("details"):
        lines.append(">\n" + quote(f"*{spec['details']}*"))
    opts = [o.get("label", o) if isinstance(o, dict) else o for o in spec.get("options", [])]
    if opts:
        lines.append(">")
        lines += [f"> - {o}" for o in opts]
    lines.append(">")
    if result is None:
        lines.append("> _aguardando resposta…_")
    elif result.startswith("User cancelled") or "timed out" in result or result.startswith(("Quiz unavailable", "Invalid quiz")):
        lines.append("> _quiz não respondido_")
    else:
        if "I don't know" in result:
            verdict = f"🤷 **Não sei** — correta: {strip_index(fields.get('Correct', ''))}"
        elif "answered correctly" in result:
            verdict = f"✅ **Correto** — {strip_index(fields.get('Selected', ''))}"
        else:
            verdict = (f"❌ **Incorreto** — respondi: {strip_index(fields.get('Selected', ''))} · "
                       f"correta: {strip_index(fields.get('Correct', ''))}")
        lines.append("> " + verdict)
        if fields.get("User's note"):
            lines.append(f"> *Minha nota:* {fields['User\'s note']}")
        if fields.get("Explanation"):
            lines.append(">\n" + quote(fields["Explanation"].strip()))
    return "\n".join(lines)


def render_ask(call: dict, result: str | None) -> str:
    qs = (call.get("input") or {}).get("questions") or []
    lines = ["> [!info] Pergunta"]
    for q in qs:
        lines.append(quote(f"**{q.get('question', '')}**"))
        opts = [o.get("label", "") for o in q.get("options", []) if isinstance(o, dict)]
        if opts:
            lines.append("> " + " · ".join(opts))
    lines.append(">")
    if result is None:
        lines.append("> _aguardando resposta…_")
    else:
        answer = re.sub(r"^User has answered your questions?:\s*", "", result.strip())
        answer = re.sub(r"\s*You can now continue.*$", "", answer, flags=re.S)
        lines.append(quote("→ " + answer))
    return "\n".join(lines)


def render(items: list[tuple], results: dict, session_id: str, first_ts: str | None) -> str:
    try:
        started = datetime.fromisoformat(first_ts.replace("Z", "+00:00")).astimezone().strftime("%Y-%m-%d %H:%M")
    except (AttributeError, ValueError):
        started = datetime.now().strftime("%Y-%m-%d %H:%M")
    out = [
        "---",
        "tags: [sessão]",
        f"sessao: {session_id}",
        f"inicio: {started}",
        f"atualizado: {datetime.now():%Y-%m-%d %H:%M}",
        "---",
        f"# Sessão {started}",
        "",
        "> [!note] Registro bruto, gerado automaticamente. O conteúdo consolidado fica em `Aulas/` e `Conceitos/`.",
    ]
    for kind, payload in items:
        out.append("")
        if kind == "user":
            out += ["### Você", payload]
        elif kind == "assistant":
            out += ["### Claude", payload]
        elif kind == "quiz":
            out.append(render_quiz(payload, results.get(payload.get("id"))))
        elif kind == "ask":
            out.append(render_ask(payload, results.get(payload.get("id"))))
    return "\n".join(out) + "\n"


# ── commands ─────────────────────────────────────────────────────────────────


def cmd_hook() -> int:
    try:
        event = json.loads(sys.stdin.read() or "{}")
        session_id = event.get("session_id")
        transcript = event.get("transcript_path")
        if not session_id or not transcript:
            return 0
        state = load_state()
        note = state["sessions"].get(session_id)
        if not note and state.get("pending"):
            note = state["sessions"][session_id] = state.pop("pending")
            state["pending"] = None
            save_state(state)
        if not note:
            return 0
        items, results, first_ts = parse_transcript(Path(transcript))
        note = Path(note)
        note.parent.mkdir(parents=True, exist_ok=True)
        tmp = note.with_name(note.name + ".tmp")
        tmp.write_text(render(items, results, session_id, first_ts), encoding="utf-8")
        tmp.replace(note)
    except Exception:  # never break the session over logging
        pass
    return 0


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "hook":
        return cmd_hook()
    state = load_state()
    sid = current_session()
    if cmd == "link":
        note = str(resolve_note(sys.argv[2] if len(sys.argv) > 2 else None))
        if sid:
            state["sessions"][sid] = note
        else:
            state["pending"] = note
        save_state(state)
        print(f"Logging this session to: {note}\n(the note is written at the end of this turn, with the whole session so far)")
        return 0
    if cmd == "off":
        note = state["sessions"].pop(sid, None) if sid else state.get("pending")
        state["pending"] = None
        save_state(state)
        print(f"Logging stopped: {note}" if note else "This session was not being logged.")
        return 0
    if cmd == "status":
        note = state["sessions"].get(sid) if sid else state.get("pending")
        print(f"Logging to: {note}" if note else "Not logging this session.")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
