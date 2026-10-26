"""Загрузка и разбор индекса пакетов Alpine Linux (APKINDEX)."""
import io
import re
import tarfile
import urllib.error
import urllib.request
from dataclasses import dataclass, field

from src.errors import RepoError

INDEX_ARCHIVE = "APKINDEX.tar.gz"
INDEX_MEMBER = "APKINDEX"
REQUEST_TIMEOUT = 30
NEGATION_PREFIX = "!"
VIRTUAL_MARK = ":"
VERSION_TAIL_RE = re.compile(r"[<>=~].*$")


@dataclass
class Package:
    """Запись о пакете из APKINDEX."""

    name: str
    version: str = ""
    depends: list = field(default_factory=list)
    provides: list = field(default_factory=list)


def build_index_url(repo_url):
    """Получить адрес архива APKINDEX.tar.gz по адресу репозитория."""
    url = repo_url.rstrip("/")
    if url.endswith(".tar.gz"):
        return url
    return f"{url}/{INDEX_ARCHIVE}"


def download(url):
    """Скачать файл по URL и вернуть содержимое в виде байтов."""
    try:
        with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT) as resp:
            return resp.read()
    except (OSError, ValueError) as error:
        raise RepoError(f"не удалось загрузить {url}: {error}") from error


def extract_index_text(archive):
    """Достать текст файла APKINDEX из архива .tar.gz."""
    try:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
            return tar.extractfile(INDEX_MEMBER).read().decode("utf-8")
    except (tarfile.TarError, KeyError, OSError, ValueError) as error:
        raise RepoError(f"некорректный архив индекса: {error}") from error


def parse_block(block):
    """Разобрать одну запись индекса; вернуть Package или None."""
    fields = {}
    for line in block.splitlines():
        key, separator, value = line.partition(":")
        if separator:
            fields[key] = value
    if "P" not in fields:
        return None
    return Package(
        name=fields["P"],
        version=fields.get("V", ""),
        depends=fields.get("D", "").split(),
        provides=fields.get("p", "").split(),
    )


def parse_index(text):
    """Разобрать текст APKINDEX в список пакетов."""
    packages = (parse_block(block) for block in text.split("\n\n"))
    return [package for package in packages if package]


def strip_version(token):
    """Убрать из зависимости условие по версии: 'musl>=1.2' -> 'musl'."""
    return VERSION_TAIL_RE.sub("", token)


class ApkRepository:
    """Репозиторий пакетов Alpine, построенный по APKINDEX."""

    def __init__(self, packages):
        self._packages = {pkg.name: pkg for pkg in packages}
        self._providers = self._build_providers(packages)

    @classmethod
    def from_url(cls, repo_url):
        """Загрузить индекс по URL и создать репозиторий."""
        archive = download(build_index_url(repo_url))
        return cls(parse_index(extract_index_text(archive)))

    @staticmethod
    def _build_providers(packages):
        """Сопоставить виртуальные имена реальным пакетам."""
        providers = {}
        for pkg in packages:
            for token in pkg.provides:
                providers.setdefault(strip_version(token), pkg.name)
        for pkg in packages:
            providers[pkg.name] = pkg.name
        return providers

    def has_package(self, name):
        """Есть ли пакет в репозитории."""
        return name in self._packages

    def all_packages(self):
        """Имена всех пакетов репозитория."""
        return list(self._packages)

    def dependencies(self, name):
        """Прямые зависимости пакета (имена реальных пакетов)."""
        package = self._packages.get(name)
        if package is None:
            return []
        result = []
        for token in package.depends:
            dep = self._resolve(token)
            if dep and dep != name and dep not in result:
                result.append(dep)
        return result

    def _resolve(self, token):
        """Превратить токен зависимости в имя пакета (или None)."""
        if token.startswith(NEGATION_PREFIX):
            return None
        base = strip_version(token)
        if base in self._providers:
            return self._providers[base]
        return None if VIRTUAL_MARK in base else base