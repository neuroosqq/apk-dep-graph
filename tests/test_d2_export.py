"""Тесты экспорта в D2."""
import unittest

from src.d2_export import quote, to_d2


class D2ExportTest(unittest.TestCase):
    """Проверка текста диаграммы."""

    def test_edges(self):
        text = to_d2({"A": ["B"], "B": []}, "A")
        self.assertIn('"A" -> "B"', text)

    def test_root_highlight(self):
        self.assertIn("style.fill", to_d2({"A": []}, "A"))

    def test_quote_special(self):
        self.assertEqual(quote("libc-dev"), '"libc-dev"')
        self.assertEqual(quote('a"b'), '"a\\"b"')