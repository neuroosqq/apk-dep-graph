"""Обратные зависимости пакета."""
from src.graph import GraphBuilder, build_graph


def build_full_graph(repo, substring=""):
    """Построить граф по всем пакетам репозитория."""
    builder = GraphBuilder(repo.dependencies, substring)
    for name in repo.all_packages():
        builder.build(name)
    return builder.graph


def invert_graph(graph):
    """Развернуть рёбра графа: 'A -> B' становится 'B -> A'."""
    inverted = {name: [] for name in graph}
    for name, deps in graph.items():
        for dep in deps:
            inverted.setdefault(dep, []).append(name)
    return inverted


def build_reverse_graph(repo, target, substring=""):
    """Вернуть (граф, циклы) обратных зависимостей пакета."""
    inverted = invert_graph(build_full_graph(repo, substring))
    return build_graph(target, lambda name: inverted.get(name, []))