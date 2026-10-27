"""Разбор и проверка параметров командной строки."""
import argparse
import os
import re
from urllib.parse import urlparse

from src.config import Config
from src.errors import ConfigError

PACKAGE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")
TEST_PACKAGE_RE = re.compile(r"^[A-Z]+$")
ALLOWED_SCHEMES = ("http", "https")


def add_input_options(parser):
    """Добавить параметры источника данных."""
    parser.add_argument(
        "-p", "--package", required=True,
        help="имя анализируемого пакета",
    )
    parser.add_argument(
        "-r", "--repo", required=True,
        help="URL репозитория или путь к файлу тестового репозитория",
    )
    parser.add_argument(
        "-t", "--test-mode", action="store_true",
        help="тестовый режим: --repo это путь к файлу описания графа",
    )
    parser.add_argument(
        "-f", "--filter", dest="filter_substr", default="",
        help="не учитывать пакеты, в имени которых есть подстрока",
    )


def add_output_options(parser):
    parser.add_argument(
        "--reverse", action="store_true",
        help="вывести обратные зависимости (кто зависит от пакета)",
    )


def build_parser():
    """Создать парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog="depgraph",
        description="Граф зависимостей пакетов Alpine Linux (apk).",
    )
    add_input_options(parser)
    add_output_options(parser)
    return parser


def validate_package(name, test_mode):
    """Проверить имя пакета."""
    pattern = TEST_PACKAGE_RE if test_mode else PACKAGE_RE
    if pattern.match(name):
        return
    hint = "A-Z" if test_mode else "A-Za-z0-9._+-"
    raise ConfigError(
        f"недопустимое имя пакета {name!r} (разрешено: {hint})"
    )


def validate_url(url):
    """Проверить, что строка является http(s)-адресом."""
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES or not parsed.netloc:
        raise ConfigError(f"некорректный URL репозитория: {url!r}")


def validate_test_file(path):
    """Проверить, что файл тестового репозитория существует."""
    if not os.path.isfile(path):
        raise ConfigError(f"файл тестового репозитория не найден: {path}")


def validate_repo(repo, test_mode):
    """Проверить параметр --repo в зависимости от режима."""
    if test_mode:
        validate_test_file(repo)
    else:
        validate_url(repo)


def validate_filter(substring, package):
    """Проверить подстроку фильтрации."""
    if any(char.isspace() for char in substring):
        raise ConfigError("подстрока фильтра не должна содержать пробелов")
    if substring and substring in package:
        raise ConfigError(
            "подстрока фильтра входит в имя анализируемого пакета"
        )


def parse_config(argv=None):
    """Разобрать аргументы и вернуть проверенную конфигурацию."""
    args = build_parser().parse_args(argv)
    validate_package(args.package, args.test_mode)
    validate_repo(args.repo, args.test_mode)
    validate_filter(args.filter_substr, args.package)
    return Config(**vars(args))

