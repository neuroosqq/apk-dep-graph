"""Вывод графа зависимостей в виде ASCII-дерева."""

MIDDLE_BRANCH = "|-- "
LAST_BRANCH = "`-- "
MIDDLE_INDENT = "|   "
LAST_INDENT = "    "
CYCLE_NOTE = " (цикл)"
SEEN_NOTE = " (см. выше)"


class TreePrinter:
    """Строит текстовое дерево; повторы и циклы не раскрывает."""

    def __init__(self, graph):
        self._graph = graph
        self._lines = []
        self._expanded = set()

    def render(self, root):
        """Вернуть дерево зависимостей корня в виде строки."""
        self._lines = [root]
        self._expanded = {root}
        self._walk(root, "", [root])
        return "\n".join(self._lines)

    def _walk(self, node, prefix, path):
        """Рекурсивно добавить потомков узла в вывод."""
        children = self._graph.get(node, [])
        count = len(children)
        for position, child in enumerate(children, start=1):
            is_last = position == count
            note = self._note(child, path)
            branch = LAST_BRANCH if is_last else MIDDLE_BRANCH
            self._lines.append(f"{prefix}{branch}{child}{note}")
            if note:
                continue
            self._expanded.add(child)
            indent = LAST_INDENT if is_last else MIDDLE_INDENT
            self._walk(child, prefix + indent, path + [child])

    def _note(self, child, path):
        """Пометка для цикла или уже показанного пакета."""
        if child in path:
            return CYCLE_NOTE
        if child in self._expanded:
            return SEEN_NOTE
        return ""