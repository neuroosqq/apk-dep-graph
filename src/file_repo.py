"""Тестовый репозиторий: граф пакетов из текстового файла.

Формат строки: "A: B C" (пакет A зависит от B и C).
"""
import re

from src.errors import RepoError

NAME_RE = re.compile(r"^[A-Z]+$")
SEPARATOR = ":"


def parse_line(line, number):
    """Разобрать строку 'A: B C' в пару (имя, список зависимостей)."""
    name, separator, rest = line.partition(SEPARATOR)
    name = name.strip()
    if not separator or not NAME_RE.match(name):
        raise RepoError(f"строка {number}: ожидается формат 'A: B C'")
    deps = rest.split()
    for dep in deps:
        if not NAME_RE.match(dep):
            raise RepoError(f"строка {number}: недопустимое имя {dep!r}")
    return name, deps


def parse_lines(lines):
    """Разобрать строки файла в словарь 'пакет -> зависимости'."""
    graph = {}
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        name, deps = parse_line(line, number)
        graph.setdefault(name, [])
        for dep in deps:
            if dep not in graph[name]:
                graph[name].append(dep)
            graph.setdefault(dep, [])
    return graph


class FileRepository:
    """Репозиторий, прочитанный из файла описания графа."""

    def __init__(self, graph):
        self._graph = graph

    @classmethod
    def from_file(cls, path):
        """Прочитать репозиторий из файла."""
        try:
            with open(path, encoding="utf-8") as source:
                lines = source.read().splitlines()
        except OSError as error:
            raise RepoError(f"не удалось прочитать {path}: {error}") from error
        return cls(parse_lines(lines))

    def has_package(self, name):
        """Есть ли пакет в репозитории."""
        return name in self._graph

    def all_packages(self):
        """Имена всех пакетов."""
        return list(self._graph)

    def dependencies(self, name):
        """Прямые зависимости пакета."""
        return list(self._graph.get(name, []))