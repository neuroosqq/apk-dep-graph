"""Тесты ASCII-дерева."""
import unittest

from src.ascii_tree import TreePrinter


class TreePrinterTest(unittest.TestCase):
    """Проверка отрисовки дерева, повторов и циклов."""

    def test_diamond(self):
        graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
        expected = "\n".join([
            "A",
            "|-- B",
            "|   `-- D",
            "`-- C",
            "    `-- D (см. выше)",
        ])
        self.assertEqual(TreePrinter(graph).render("A"), expected)

    def test_cycle(self):
        graph = {"A": ["B"], "B": ["A"]}
        expected = "A\n`-- B\n    `-- A (цикл)"
        self.assertEqual(TreePrinter(graph).render("A"), expected)

    def test_single_node(self):
        self.assertEqual(TreePrinter({"A": []}).render("A"), "A")