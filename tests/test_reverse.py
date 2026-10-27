"""Тесты обратных зависимостей."""
import unittest

from src.file_repo import FileRepository
from src.reverse import build_reverse_graph, invert_graph


class ReverseTest(unittest.TestCase):
    """Проверка инверсии и обхода обратного графа."""

    def test_invert(self):
        graph = {"A": ["B"], "B": []}
        self.assertEqual(invert_graph(graph), {"A": [], "B": ["A"]})

    def test_diamond(self):
        repo = FileRepository(
            {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
        )
        graph, cycles = build_reverse_graph(repo, "D")
        self.assertEqual(
            graph, {"D": ["B", "C"], "B": ["A"], "A": [], "C": ["A"]}
        )
        self.assertEqual(cycles, [])

    def test_cycle(self):
        repo = FileRepository({"A": ["B"], "B": ["A"]})
        _, cycles = build_reverse_graph(repo, "A")
        self.assertEqual(len(cycles), 1)

    def test_filter(self):
        repo = FileRepository({"A": ["B"], "B": []})
        graph, _ = build_reverse_graph(repo, "B", "A")
        self.assertEqual(graph, {"B": []})