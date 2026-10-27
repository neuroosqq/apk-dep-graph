"""Точка входа приложения."""
import sys
from src.reverse import build_reverse_graph
from src.apk_repo import ApkRepository
from src.cli import parse_config
from src.errors import AppError, RepoError
from src.file_repo import FileRepository
from src.graph import build_graph

EXIT_OK = 0
EXIT_ERROR = 1
NO_DEPS = "-"


def open_repository(config):
    """Создать репозиторий в зависимости от режима работы."""
    if config.test_mode:
        return FileRepository.from_file(config.repo)
    return ApkRepository.from_url(config.repo)


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


def build_result_graph(config, repo):
    """Построить прямой или обратный граф зависимостей."""
    if config.reverse:
        return build_reverse_graph(
            repo, config.package, config.filter_substr
        )
    return build_graph(
        config.package, repo.dependencies, config.filter_substr
    )


def run(config):
    """Построить и вывести граф зависимостей."""
    repo = open_repository(config)
    if not repo.has_package(config.package):
        raise RepoError(f"пакет {config.package!r} не найден")
    graph, cycles = build_result_graph(config, repo)
    title = "Обратные зависимости" if config.reverse else "Зависимости"
    print(f"{title} пакета {config.package}:")
    print_graph(graph)
    print_cycles(cycles)


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