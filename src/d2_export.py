"""Экспорт графа зависимостей на язык диаграмм D2."""

ROOT_FILL = "#ffe699"


def quote(name):
    """Заключить имя в кавычки (в имени могут быть . - +)."""
    escaped = name.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def to_d2(graph, root):
    """Сформировать текст диаграммы D2 по графу зависимостей."""
    lines = ["direction: right"]
    lines.extend(quote(name) for name in graph)
    lines.append(f"{quote(root)}: {{")
    lines.append(f'  style.fill: "{ROOT_FILL}"')
    lines.append("}")
    for name, deps in graph.items():
        lines.extend(f"{quote(name)} -> {quote(dep)}" for dep in deps)
    return "\n".join(lines) + "\n"