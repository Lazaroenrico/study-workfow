#!/usr/bin/env python3
"""quiz — a graded multiple-choice question shown in a popup terminal.

Port of the `quiz` extension from amosblomqvist/learn (pi) to Claude Code, where
the Bash tool has no TTY: this script opens the UI in a separate floating
terminal, waits for the answer, grades it deterministically and prints the
result for the agent.

Usage (from Claude Code, via Bash with timeout 600000):

    python3 .claude/tools/quiz.py <<'EOF'
    {"question": "...", "details": "...",
     "options": [{"label": "...", "value": "a", "description": "..."}, ...],
     "correctAnswer": "a", "explanation": "...",
     "multiSelect": false, "shuffle": true, "topic": "..."}
    EOF

Curriculum lessons (questions come from the lesson's quiz.json, so the answer key never
appears in the command):

    python3 .claude/tools/quiz.py --lesson curriculum/phases/<phase>/<lesson> --count
    python3 .claude/tools/quiz.py --lesson curriculum/phases/<phase>/<lesson> --stage pre --index 0

Where the UI opens:
  - inside tmux: a `tmux display-popup`;
  - otherwise: `foot --app-id=TUI.float` (Omarchy floats and centers that app-id),
    falling back to `xdg-terminal-exec`.

Every quiz (answered or not) is appended to .claude/state/quiz-log.jsonl.

Exit codes: 0 = result printed (answered / cancelled / unavailable), 2 = invalid spec.
"""

from __future__ import annotations

import curses
import json
import locale
import os
import random
import shlex
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
from datetime import datetime
from pathlib import Path

STATE_DIR = Path(__file__).resolve().parent.parent / "state"
LOG_FILE = STATE_DIR / "quiz-log.jsonl"
# Stay under the Bash tool's 10-minute ceiling so we always print a result.
TIMEOUT_S = 570
DONT_KNOW_LABEL = "Não sei"


class SpecError(Exception):
    pass


# ── spec validation ──────────────────────────────────────────────────────────


def normalize_options(raw) -> list[dict]:
    if not isinstance(raw, list):
        raise SpecError("options must be a list")
    seen: set[str] = set()
    out: list[dict] = []
    for opt in raw:
        if isinstance(opt, str):
            opt = {"label": opt}
        if not isinstance(opt, dict):
            raise SpecError("each option must be an object with a label")
        label = str(opt.get("label", "")).strip()
        if not label:
            continue
        value = str(opt.get("value") or label).strip()
        if value in seen:
            raise SpecError(f'duplicate option value "{value}"')
        seen.add(value)
        description = str(opt.get("description") or "").strip() or None
        out.append({"label": label, "value": value, "description": description})
    if len(out) < 2:
        raise SpecError("at least 2 options are required")
    return out


def coerce_correct(correct) -> list[str]:
    """Accept a value, a list of values, or a JSON-stringified list of values."""
    if correct is None:
        return []
    if isinstance(correct, list):
        return [str(v).strip() for v in correct]
    text = str(correct).strip()
    if text.startswith("[") and text.endswith("]"):
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return [str(v).strip() for v in parsed]
        except json.JSONDecodeError:
            pass
    return [text] if text else []


def prepare(spec, rng: random.Random | None = None) -> dict:
    """Validate a spec and fix the display order. Raises SpecError."""
    if not isinstance(spec, dict):
        raise SpecError("spec must be a JSON object")
    question = str(spec.get("question", "")).strip()
    if not question:
        raise SpecError("question is required")
    options = normalize_options(spec.get("options"))
    correct = coerce_correct(spec.get("correctAnswer"))
    if not correct:
        raise SpecError("correctAnswer is required")
    values = [o["value"] for o in options]
    for v in correct:
        if v not in values:
            known = ", ".join(f'"{x}"' for x in values)
            raise SpecError(f'correctAnswer "{v}" does not match any option value ({known})')
    multi = bool(spec.get("multiSelect", False))
    if not multi and len(set(correct)) > 1:
        raise SpecError("single-select quiz needs exactly one correctAnswer (or set multiSelect: true)")
    explanation = str(spec.get("explanation", "")).strip()
    if not explanation:
        raise SpecError("explanation is required")
    if spec.get("shuffle", True):
        (rng or random).shuffle(options)
    return {
        "question": question,
        "details": str(spec.get("details") or "").strip() or None,
        "topic": str(spec.get("topic") or "").strip() or None,
        "options": options,
        "correct": sorted(set(correct), key=[o["value"] for o in options].index),
        "multiSelect": multi,
        "explanation": explanation,
    }


# ── grading and result text ──────────────────────────────────────────────────


def index_of(prepared: dict, value: str) -> int:
    """1-based display index of an option value."""
    return [o["value"] for o in prepared["options"]].index(value) + 1


def is_correct(prepared: dict, response: dict) -> bool:
    if response.get("dontKnow"):
        return False
    return set(response.get("selected", [])) == set(prepared["correct"])


def option_ref(prepared: dict, value: str) -> str:
    i = index_of(prepared, value)
    return f"{i}. {prepared['options'][i - 1]['label']}"


def format_result(prepared: dict, response: dict) -> str:
    status = response.get("status")
    head = f"Question: {prepared['question'].splitlines()[0]}\n"
    if status == "cancelled":
        return head + "User cancelled the quiz"
    if status == "timeout":
        return head + f"Quiz timed out after {TIMEOUT_S}s without an answer (treat as cancelled)"
    if status == "unavailable":
        return head + f"Quiz unavailable: {response.get('message', 'no UI could be opened')}"

    correct_str = ", ".join(option_ref(prepared, v) for v in prepared["correct"])
    note = response.get("note")
    if response.get("dontKnow"):
        text = ('User selected "I don\'t know" — they did not attempt an answer '
                "(a genuine knowledge gap, not a wrong guess).")
        text += f"\nCorrect: {correct_str}"
    else:
        verdict = "correctly" if is_correct(prepared, response) else "incorrectly"
        selected = sorted(response.get("selected", []), key=lambda v: index_of(prepared, v))
        selected_str = ", ".join(option_ref(prepared, v) for v in selected)
        text = f"User answered {verdict}.\nSelected: {selected_str}\nCorrect: {correct_str}"
    if note:
        text += f"\nUser's note: {note}"
    text += f"\nExplanation: {prepared['explanation']}"
    return head + text


def log_entry(prepared: dict, response: dict) -> dict:
    answered = response.get("status") == "answered"
    return {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "topic": prepared["topic"],
        "question": prepared["question"],
        "options": [o["label"] for o in prepared["options"]],
        "correct": [option_ref(prepared, v) for v in prepared["correct"]],
        "status": response.get("status"),
        "selected": [option_ref(prepared, v) for v in response.get("selected", [])] if answered else [],
        "dontKnow": bool(response.get("dontKnow")) if answered else None,
        "isCorrect": is_correct(prepared, response) if answered else None,
        "note": response.get("note"),
    }


def append_log(entry: dict) -> None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass  # logging must never break the quiz


# ── launching the popup ──────────────────────────────────────────────────────


def launcher_argv(ui_cmd: list[str]) -> tuple[list[str] | None, bool, str | None]:
    """Return (argv, blocks_until_done, error)."""
    if os.environ.get("TMUX") and shutil.which("tmux"):
        argv = ["tmux", "display-popup", "-E", "-w", "90%", "-h", "85%", "-T", " quiz ", shlex.join(ui_cmd)]
        return argv, True, None
    if os.environ.get("WAYLAND_DISPLAY") or os.environ.get("DISPLAY"):
        if shutil.which("foot"):
            return ["foot", "--app-id=TUI.float", "--title=quiz", *ui_cmd], True, None
        if shutil.which("xdg-terminal-exec"):
            return ["xdg-terminal-exec", "--app-id=TUI.float", "--title=quiz", *ui_cmd], False, None
        return None, False, "no terminal emulator found (foot / xdg-terminal-exec)"
    return None, False, "no graphical session or tmux session to open the quiz in"


def run_popup(prepared: dict) -> dict:
    with tempfile.TemporaryDirectory(prefix="quiz-") as tmp:
        spec_path = Path(tmp, "spec.json")
        result_path = Path(tmp, "result.json")
        spec_path.write_text(json.dumps(prepared, ensure_ascii=False), encoding="utf-8")
        ui_cmd = [sys.executable, str(Path(__file__).resolve()), "--ui", str(spec_path), str(result_path)]
        argv, blocks, error = launcher_argv(ui_cmd)
        if argv is None:
            return {"status": "unavailable", "message": error}

        proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, start_new_session=True)
        deadline = time.monotonic() + TIMEOUT_S
        while time.monotonic() < deadline:
            if result_path.exists():
                break
            # A blocking launcher that exited without a result = window closed.
            if blocks and proc.poll() is not None:
                break
            time.sleep(0.2)
        else:
            proc.kill()
            return {"status": "timeout"}

        if result_path.exists():
            try:
                return json.loads(result_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                pass
        return {"status": "cancelled"}


LESSON_LETTERS = "abcdefghijklmnopqrstuvwxyz"


def lesson_questions(lesson_dir: Path) -> list[dict]:
    data = json.loads((lesson_dir / "quiz.json").read_text(encoding="utf-8"))
    return data.get("questions", []) if isinstance(data, dict) else data


def lesson_spec(lesson_dir: Path, stage: str, index: int) -> dict:
    """Turn one quiz.json question (options: [str], correct: 0-based int) into a quiz spec."""
    questions = [q for q in lesson_questions(lesson_dir) if q.get("stage") == stage]
    if not questions:
        raise SpecError(f'no questions with stage "{stage}" in {lesson_dir / "quiz.json"}')
    if not 0 <= index < len(questions):
        raise SpecError(f'--index {index} out of range: stage "{stage}" has {len(questions)} questions (0-{len(questions) - 1})')
    q = questions[index]
    options = [{"label": str(label), "value": LESSON_LETTERS[i]} for i, label in enumerate(q.get("options", []))]
    correct = q.get("correct")
    if not isinstance(correct, int) or not 0 <= correct < len(options):
        raise SpecError(f"question {index} has an invalid correct index: {correct!r}")
    return {
        "topic": lesson_dir.name,
        "question": q.get("question", ""),
        "details": f"Aula {lesson_dir.parent.name}/{lesson_dir.name} · {stage} {index + 1}/{len(questions)}",
        "options": options,
        "correctAnswer": options[correct]["value"],
        "explanation": (q.get("explanation") or "").strip() or "(O quiz da aula não traz explicação para esta pergunta.)",
    }


def lesson_counts(lesson_dir: Path) -> str:
    counts: dict[str, int] = {}
    for q in lesson_questions(lesson_dir):
        counts[q.get("stage", "?")] = counts.get(q.get("stage", "?"), 0) + 1
    return ", ".join(f"{stage}: {n}" for stage, n in counts.items()) or "no questions"


def parse_lesson_args(argv: list[str]) -> tuple[Path, str | None, int, bool]:
    lesson, stage, index, count = None, None, 0, False
    it = iter(argv)
    for a in it:
        if a == "--lesson":
            lesson = Path(next(it, ""))
        elif a == "--stage":
            stage = next(it, None)
        elif a == "--index":
            index = int(next(it, "0"))
        elif a == "--count":
            count = True
    if lesson is None or not (lesson / "quiz.json").is_file():
        raise SpecError(f"lesson has no quiz.json: {lesson}")
    if not count and stage is None:
        raise SpecError("--stage is required (pre, check or post)")
    return lesson, stage, index, count


def main_cli(argv: list[str]) -> int:
    try:
        if argv and argv[0] == "--lesson":
            lesson, stage, index, count = parse_lesson_args(argv)
            if count:
                print(f"{lesson.name}: {lesson_counts(lesson)}")
                return 0
            spec = lesson_spec(lesson, stage, index)
        else:
            spec = json.loads(sys.stdin.read())
        prepared = prepare(spec)
    except json.JSONDecodeError as e:
        print(f"Invalid quiz spec: not valid JSON ({e})")
        return 2
    except (SpecError, ValueError, OSError) as e:
        print(f"Invalid quiz spec: {e}")
        return 2
    response = run_popup(prepared)
    append_log(log_entry(prepared, response))
    print(format_result(prepared, response))
    return 0


# ── curses UI (runs inside the popup) ────────────────────────────────────────


class QuizUI:
    def __init__(self, prepared: dict):
        self.q = prepared
        self.n = len(prepared["options"])
        self.focus = 0  # 0..n-1 options, n = "Não sei", n+1 = note field
        self.selected: list[str] = []
        self.note = ""
        self.message = ""
        self.response: dict | None = None
        self.scroll = 0
        self.prev_focus = 0

    # styles
    def _init_colors(self):
        self.c = {k: curses.A_NORMAL for k in ("ok", "bad", "warn", "accent")}
        self.c["dim"] = curses.A_DIM
        if curses.has_colors():
            curses.start_color()
            try:
                curses.use_default_colors()
                bg = -1
            except curses.error:
                bg = curses.COLOR_BLACK
            for i, (k, fg) in enumerate([("ok", curses.COLOR_GREEN), ("bad", curses.COLOR_RED),
                                         ("warn", curses.COLOR_YELLOW), ("accent", curses.COLOR_CYAN)], 1):
                curses.init_pair(i, fg, bg)
                self.c[k] = curses.color_pair(i)

    def run(self, scr) -> dict:
        curses.curs_set(0)
        self._init_colors()
        scr.keypad(True)
        while True:
            self.draw(scr)
            try:
                key = scr.get_wch()
            except curses.error:
                continue
            if self.response is None:
                if self.handle_select(key) == "cancel":
                    return {"status": "cancelled"}
            else:
                if key in ("\n", "\r", "\x1b", "q", " ", curses.KEY_ENTER):
                    return self.response
                self.handle_scroll(key)

    # input
    def handle_scroll(self, key):
        if key in (curses.KEY_UP, "k"):
            self.scroll = max(0, self.scroll - 1)
        elif key in (curses.KEY_DOWN, "j"):
            self.scroll += 1

    def handle_select(self, key):
        self.message = ""
        if self.focus == self.n + 1:  # typing in the note field
            if key in ("\x1b", "\t", curses.KEY_BTAB, "\n", "\r", curses.KEY_ENTER):
                self.focus = self.prev_focus
            elif key == curses.KEY_UP:
                self.focus = self.n
            elif key in (curses.KEY_BACKSPACE, "\x7f", "\b"):
                self.note = self.note[:-1]
            elif isinstance(key, str) and key.isprintable():
                self.note += key
            return None
        if key == "\x1b" or key == "q":
            return "cancel"
        if key in (curses.KEY_UP, "k"):
            self.focus = max(0, self.focus - 1)
        elif key in (curses.KEY_DOWN, "j"):
            if self.focus == self.n:
                self.prev_focus = self.n
            self.focus = min(self.n + 1, self.focus + 1)
        elif key in ("\t", curses.KEY_BTAB):
            self.prev_focus, self.focus = self.focus, self.n + 1
        elif isinstance(key, str) and key.isdigit() and 1 <= int(key) <= min(self.n, 9):
            self.focus = int(key) - 1
            if self.q["multiSelect"]:
                self.toggle(self.focus)
        elif key == " " and self.q["multiSelect"] and self.focus < self.n:
            self.toggle(self.focus)
        elif key in ("\n", "\r", curses.KEY_ENTER):
            self.submit()
        return None

    def toggle(self, i):
        v = self.q["options"][i]["value"]
        if v in self.selected:
            self.selected.remove(v)
        else:
            self.selected.append(v)

    def submit(self):
        note = self.note.strip() or None
        if self.focus == self.n:
            self.response = {"status": "answered", "dontKnow": True, "selected": [], "note": note}
        elif self.q["multiSelect"]:
            if not self.selected:
                self.message = "Marque ao menos uma opção com espaço (ou escolha “Não sei”)."
                return
            self.response = {"status": "answered", "dontKnow": False, "selected": list(self.selected), "note": note}
        else:
            v = self.q["options"][self.focus]["value"]
            self.response = {"status": "answered", "dontKnow": False, "selected": [v], "note": note}
        self.scroll = 0

    # drawing
    def lines(self, width) -> tuple[list[tuple[str, int]], int]:
        """Build (text, attr) lines and return them with the line index to keep visible."""
        out: list[tuple[str, int]] = []
        w = max(10, width - 2)

        def add(text, attr=curses.A_NORMAL, indent=""):
            for line in textwrap.wrap(text, w - len(indent)) or [""]:
                out.append((indent + line, attr))

        out.append(("─" * w, self.c["accent"]))
        for para in self.q["question"].splitlines() or [""]:
            add(para, curses.A_BOLD)
        if self.q["details"]:
            out.append(("", 0))
            for para in self.q["details"].splitlines():
                add(para, self.c["dim"])
        out.append(("", 0))
        if self.q["multiSelect"]:
            add("(várias corretas — marque todas)", self.c["warn"])
            out.append(("", 0))

        focus_line = 0
        answered = self.response is not None
        dont_know = answered and self.response.get("dontKnow")
        chosen = set(self.response.get("selected", [])) if answered else set(self.selected)
        correct = set(self.q["correct"])
        for i, opt in enumerate(self.q["options"]):
            v = opt["value"]
            if not answered:
                pointer = "›" if self.focus == i else " "
                box = ("[x] " if v in chosen else "[ ] ") if self.q["multiSelect"] else ""
                attr = self.c["accent"] | curses.A_BOLD if self.focus == i else curses.A_NORMAL
                if self.focus == i:
                    focus_line = len(out)
                add(f"{pointer} {i + 1}. {box}{opt['label']}", attr)
            else:
                if v in correct:
                    mark, attr = "✓", self.c["ok"]
                elif v in chosen and not dont_know:
                    mark, attr = "✗", self.c["bad"]
                else:
                    mark, attr = " ", self.c["dim"]
                add(f"{mark} {i + 1}. {opt['label']}", attr)
            if opt["description"]:
                add(opt["description"], self.c["dim"], indent="      ")

        if not answered:
            out.append(("", 0))
            if self.focus == self.n:
                focus_line = len(out)
            attr = self.c["accent"] | curses.A_BOLD if self.focus == self.n else self.c["dim"]
            add(f"{'›' if self.focus == self.n else ' '} {DONT_KNOW_LABEL}", attr)
            out.append(("", 0))
            if self.focus == self.n + 1:
                focus_line = len(out)
            label = "Nota (opcional): "
            attr = self.c["accent"] if self.focus == self.n + 1 else self.c["dim"]
            add(label + self.note + ("▏" if self.focus == self.n + 1 else ""), attr)
            if self.message:
                out.append(("", 0))
                add(self.message, self.c["warn"])
            out.append(("", 0))
            keys = "↑↓ mover · 1-9 ir · " + ("espaço marcar · " if self.q["multiSelect"] else "")
            add(keys + "Enter responder · Tab nota · Esc cancelar", self.c["dim"])
            if self.focus == self.n + 1:
                add("(digitando a nota — Enter/Tab/Esc volta para as opções)", self.c["dim"])
        else:
            out.append(("", 0))
            if dont_know:
                add("· Você disse: Não sei", self.c["warn"])
            elif is_correct(self.q, self.response):
                add("✓ Correto!", self.c["ok"] | curses.A_BOLD)
            else:
                add("✗ Incorreto.", self.c["bad"] | curses.A_BOLD)
            if dont_know or not is_correct(self.q, self.response):
                add("Resposta correta: " + ", ".join(option_ref(self.q, v) for v in self.q["correct"]), self.c["dim"])
            if self.response.get("note"):
                add("Sua nota: " + self.response["note"], self.c["dim"])
            out.append(("", 0))
            for para in self.q["explanation"].splitlines():
                add(para)
            out.append(("", 0))
            add("Enter/Esc para fechar · ↑↓ rolar", self.c["dim"])
        return out, focus_line

    def draw(self, scr):
        scr.erase()
        height, width = scr.getmaxyx()
        out, focus_line = self.lines(width)
        if self.response is None:
            # keep the focused line visible
            if focus_line < self.scroll:
                self.scroll = focus_line
            elif focus_line >= self.scroll + height - 1:
                self.scroll = focus_line - height + 2
        self.scroll = max(0, min(self.scroll, max(0, len(out) - height)))
        for row, (text, attr) in enumerate(out[self.scroll:self.scroll + height]):
            try:
                scr.addnstr(row, 1, text, width - 2, attr)
            except curses.error:
                pass
        scr.refresh()


def main_ui(spec_path: str, result_path: str) -> int:
    locale.setlocale(locale.LC_ALL, "")
    os.environ.setdefault("ESCDELAY", "25")
    prepared = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    try:
        response = curses.wrapper(QuizUI(prepared).run)
    except KeyboardInterrupt:
        response = {"status": "cancelled"}
    tmp = result_path + ".tmp"
    Path(tmp).write_text(json.dumps(response, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, result_path)
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--ui":
        sys.exit(main_ui(sys.argv[2], sys.argv[3]))
    sys.exit(main_cli(sys.argv[1:]))
