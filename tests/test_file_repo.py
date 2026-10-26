"""Тесты тестового репозитория из файла."""
import unittest

from src.errors import RepoError
from src.file_repo import FileRepository, parse_lines


class FileRepositoryTest(unittest.TestCase):
    """Проверка разбора файла описания графа."""

    def test_parse(self):
        graph = parse_lines(["A: B C", "", "B: C"])
        self.assertEqual(graph, {"A": ["B", "C"], "B": ["C"], "C": []})

    def test_bad_name(self):
        with self.assertRaises(RepoError):
            parse_lines(["a: B"])

    def test_missing_separator(self):
        with self.assertRaises(RepoError):
            parse_lines(["A B"])

    def test_missing_file(self):
        with self.assertRaises(RepoError):
            FileRepository.from_file("tests/data/absent.txt")