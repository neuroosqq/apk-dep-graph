"""Точка входа приложения."""
import sys

from src.apk_repo import ApkRepository
from src.cli import parse_config
from src.errors import AppError, RepoError

EXIT_OK = 0
EXIT_ERROR = 1


def run(config):
    """Вывести прямые зависимости пакета (только этап 2)."""
    repo = ApkRepository.from_url(config.repo)
    if not repo.has_package(config.package):
        raise RepoError(f"пакет {config.package!r} не найден")
    print(f"Прямые зависимости пакета {config.package}:")
    for dep in repo.dependencies(config.package):
        print(f"  {dep}")


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