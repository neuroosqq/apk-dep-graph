"""Тесты построения графа и поиска циклов."""
import unittest

from src.graph import build_graph


def make_deps(table):
    """Создать функцию получения зависимостей по словарю."""
    return lambda name: table.get(name, [])


class BuildGraphTest(unittest.TestCase):
    """Проверка DFS, фильтрации и циклов."""

    def test_chain(self):
        graph, cycles = build_graph("A", make_deps({"A": ["B"], "B": ["C"]}))
        self.assertEqual(graph, {"A": ["B"], "B": ["C"], "C": []})
        self.assertEqual(cycles, [])

    def test_cycle(self):
        graph, cycles = build_graph("A", make_deps({"A": ["B"], "B": ["A"]}))
        self.assertEqual(graph, {"A": ["B"], "B": ["A"]})
        self.assertEqual(cycles, [["A", "B", "A"]])

    def test_self_loop(self):
        _, cycles = build_graph("A", make_deps({"A": ["A"]}))
        self.assertEqual(cycles, [["A", "A"]])

    def test_shared_dependency_visited_once(self):
        table = {"A": ["B", "C"], "B": ["D"], "C": ["D"]}
        graph, cycles = build_graph("A", make_deps(table))
        self.assertEqual(graph["D"], [])
        self.assertEqual(cycles, [])

    def test_filter(self):
        table = {"app": ["libfoo", "bar"], "bar": ["libbaz"]}
        graph, _ = build_graph("app", make_deps(table), "lib")
        self.assertEqual(graph, {"app": ["bar"], "bar": []})