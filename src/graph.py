"""Построение графа зависимостей обходом в глубину (DFS, рекурсия)."""


class GraphBuilder:
    """Строит граф зависимостей рекурсивным DFS и находит циклы."""

    def __init__(self, get_deps, substring=""):
        self._get_deps = get_deps
        self._substring = substring
        self._stack = []
        self.graph = {}
        self.cycles = []

    def build(self, root):
        """Обойти граф от корня; посещённые узлы пропускаются."""
        if root in self.graph or self._is_excluded(root):
            return
        self._visit(root)

    def _is_excluded(self, name):
        """Исключён ли пакет фильтром по подстроке."""
        return bool(self._substring) and self._substring in name

    def _visit(self, name):
        """Рекурсивно посетить пакет и его зависимости."""
        self._stack.append(name)
        self.graph[name] = []
        for dep in self._get_deps(name):
            if self._is_excluded(dep):
                continue
            self.graph[name].append(dep)
            if dep in self._stack:
                self._record_cycle(dep)
            elif dep not in self.graph:
                self._visit(dep)
        self._stack.pop()

    def _record_cycle(self, dep):
        """Запомнить цикл: участок стека от dep до конца, плюс dep."""
        start = self._stack.index(dep)
        self.cycles.append(self._stack[start:] + [dep])


def build_graph(root, get_deps, substring=""):
    """Вернуть (граф, список циклов) для корневого пакета."""
    builder = GraphBuilder(get_deps, substring)
    builder.build(root)
    return builder.graph, builder.cycles