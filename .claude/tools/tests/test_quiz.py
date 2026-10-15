"""Grading tests for quiz.py. Run: python3 -m unittest discover -s .claude/tools/tests"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import quiz  # noqa: E402

OPTS = [{"label": "Mercúrio", "value": "a"}, {"label": "Vênus", "value": "b"},
        {"label": "Terra", "value": "c"}, {"label": "Marte", "value": "d"}]


def spec(**kw):
    base = {"question": "Planeta mais próximo do Sol?", "options": OPTS,
            "correctAnswer": "a", "explanation": "Mercúrio orbita mais perto."}
    base.update(kw)
    return base


def answered(selected=(), dont_know=False, note=None):
    return {"status": "answered", "selected": list(selected), "dontKnow": dont_know, "note": note}


class Validation(unittest.TestCase):
    def test_unknown_correct_value(self):
        with self.assertRaisesRegex(quiz.SpecError, 'does not match'):
            quiz.prepare(spec(correctAnswer="z"))

    def test_duplicate_values(self):
        with self.assertRaisesRegex(quiz.SpecError, "duplicate"):
            quiz.prepare(spec(options=[{"label": "x", "value": "a"}, {"label": "y", "value": "a"}]))

    def test_needs_two_options(self):
        with self.assertRaises(quiz.SpecError):
            quiz.prepare(spec(options=[{"label": "x", "value": "a"}]))

    def test_explanation_required(self):
        with self.assertRaises(quiz.SpecError):
            quiz.prepare(spec(explanation=""))

    def test_single_select_with_two_answers(self):
        with self.assertRaisesRegex(quiz.SpecError, "multiSelect"):
            quiz.prepare(spec(correctAnswer=["a", "b"]))

    def test_stringified_array(self):
        p = quiz.prepare(spec(multiSelect=True, correctAnswer='["a", "c"]'))
        self.assertEqual(set(p["correct"]), {"a", "c"})

    def test_value_defaults_to_label(self):
        p = quiz.prepare(spec(options=["sim", "não"], correctAnswer="não"))
        self.assertEqual(p["correct"], ["não"])


class Grading(unittest.TestCase):
    def test_shuffle_keeps_grading_by_value(self):
        for seed in range(20):
            p = quiz.prepare(spec(), random.Random(seed))
            self.assertTrue(quiz.is_correct(p, answered(["a"])))
            self.assertFalse(quiz.is_correct(p, answered(["b"])))

    def test_shuffle_false_keeps_order(self):
        p = quiz.prepare(spec(shuffle=False))
        self.assertEqual([o["value"] for o in p["options"]], ["a", "b", "c", "d"])

    def test_multi_requires_exact_set(self):
        p = quiz.prepare(spec(multiSelect=True, correctAnswer=["a", "c"]))
        self.assertTrue(quiz.is_correct(p, answered(["c", "a"])))
        self.assertFalse(quiz.is_correct(p, answered(["a"])))
        self.assertFalse(quiz.is_correct(p, answered(["a", "c", "d"])))

    def test_dont_know_is_never_correct(self):
        p = quiz.prepare(spec())
        self.assertFalse(quiz.is_correct(p, answered(dont_know=True)))


class ResultText(unittest.TestCase):
    def setUp(self):
        self.p = quiz.prepare(spec(shuffle=False))

    def test_wrong_answer_text(self):
        text = quiz.format_result(self.p, answered(["b"], note="chutei"))
        self.assertTrue(text.startswith("Question: Planeta mais próximo do Sol?\n"))
        self.assertIn("User answered incorrectly.", text)
        self.assertIn("Selected: 2. Vênus", text)
        self.assertIn("Correct: 1. Mercúrio", text)
        self.assertIn("User's note: chutei", text)
        self.assertIn("Explanation: Mercúrio orbita mais perto.", text)

    def test_dont_know_text(self):
        text = quiz.format_result(self.p, answered(dont_know=True))
        self.assertIn("I don't know", text)
        self.assertIn("not a wrong guess", text)

    def test_cancelled_and_timeout(self):
        self.assertTrue(quiz.format_result(self.p, {"status": "cancelled"}).endswith("User cancelled the quiz"))
        self.assertIn("timed out", quiz.format_result(self.p, {"status": "timeout"}))

    def test_log_entry(self):
        e = quiz.log_entry(self.p, answered(["a"]))
        self.assertTrue(e["isCorrect"])
        self.assertEqual(e["selected"], ["1. Mercúrio"])
        e = quiz.log_entry(self.p, {"status": "cancelled"})
        self.assertIsNone(e["isCorrect"])


CURRICULUM = Path(__file__).resolve().parents[3] / "curriculum" / "phases"


@unittest.skipUnless(CURRICULUM.is_dir(), "curriculum not cloned")
class LessonMode(unittest.TestCase):
    def test_every_lesson_question_converts(self):
        n = 0
        for qf in CURRICULUM.glob("*/*/quiz.json"):
            by_stage: dict = {}
            for q in quiz.lesson_questions(qf.parent):
                by_stage[q.get("stage")] = by_stage.get(q.get("stage"), -1) + 1
                p = quiz.prepare(quiz.lesson_spec(qf.parent, q.get("stage"), by_stage[q.get("stage")]))
                self.assertEqual(p["correct"], [quiz.LESSON_LETTERS[q["correct"]]])
                n += 1
        self.assertGreater(n, 1000)

    def test_bad_index(self):
        lesson = next(CURRICULUM.glob("*/*/quiz.json")).parent
        with self.assertRaisesRegex(quiz.SpecError, "out of range"):
            quiz.lesson_spec(lesson, "pre", 999)


if __name__ == "__main__":
    unittest.main()
