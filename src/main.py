"""Точка входа приложения."""
import sys

from src.apk_repo import ApkRepository
from src.ascii_tree import TreePrinter
from src.cli import parse_config
from src.d2_export import to_d2
from src.errors import AppError, RepoError
from src.file_repo import FileRepository
from src.graph import build_graph
from src.renderer import render_image, show_image
from src.reverse import build_reverse_graph

EXIT_OK = 0
EXIT_ERROR = 1
NO_DEPS = "-"


def open_repository(config):
    """Создать репозиторий в зависимости от режима работы."""
    if config.test_mode:
        return FileRepository.from_file(config.repo)
    return ApkRepository.from_url(config.repo)


def build_result_graph(config, repo):
    """Построить прямой или обратный граф зависимостей."""
    if config.reverse:
        return build_reverse_graph(
            repo, config.package, config.filter_substr
        )
    return build_graph(
        config.package, repo.dependencies, config.filter_substr
    )


def print_graph(graph):
    """Вывести граф в виде списка смежности."""
    for name, deps in graph.items():
        print(f"{name} -> {', '.join(deps) if deps else NO_DEPS}")


def print_cycles(cycles):
    """Вывести найденные циклы."""
    if not cycles:
        return
    print("Обнаружены циклические зависимости:")
    for cycle in cycles:
        print("  " + " -> ".join(cycle))


def report(config, graph, cycles):
    """Вывести результат в текстовом виде."""
    title = "Обратные зависимости" if config.reverse else "Зависимости"
    print(f"{title} пакета {config.package}:")
    if config.ascii_tree:
        print(TreePrinter(graph).render(config.package))
    else:
        print_graph(graph)
    print_cycles(cycles)


def visualize(config, graph):
    """Сохранить текст D2 и показать изображение графа."""
    with open(config.d2_file, "w", encoding="utf-8") as out:
        out.write(to_d2(graph, config.package))
    if config.no_image:
        return
    render_image(config.d2_file, config.image)
    show_image(config.image)


def run(config):
    """Выполнить анализ и визуализацию."""
    repo = open_repository(config)
    if not repo.has_package(config.package):
        raise RepoError(f"пакет {config.package!r} не найден")
    graph, cycles = build_result_graph(config, repo)
    report(config, graph, cycles)
    visualize(config, graph)


def main(argv=None):
    """Запустить приложение и вернуть код завершения."""
    try:
        run(parse_config(argv))
    except AppError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return EXIT_ERROR
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())