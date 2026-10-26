"""Тесты разбора индекса Alpine."""
import io
import tarfile
import unittest

from src.apk_repo import (
    ApkRepository, build_index_url, extract_index_text, parse_index,
)
from src.errors import RepoError

SAMPLE = """P:app
V:1.0-r0
D:musl so:libz.so.1 !conflict>1 other>=2.0

P:musl
V:1.2-r0
p:so:libc.musl-x86_64.so.1=1

P:zlib
V:1.3-r0
p:so:libz.so.1=1.3
"""


def make_archive(text):
    """Собрать tar.gz с файлом APKINDEX в памяти."""
    data = text.encode("utf-8")
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        info = tarfile.TarInfo("APKINDEX")
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


class ApkRepositoryTest(unittest.TestCase):
    """Проверка разбора и разрешения зависимостей."""

    def test_index_url(self):
        self.assertEqual(
            build_index_url("http://x/main/x86_64/"),
            "http://x/main/x86_64/APKINDEX.tar.gz",
        )

    def test_extract_index(self):
        self.assertEqual(extract_index_text(make_archive(SAMPLE)), SAMPLE)

    def test_bad_archive(self):
        with self.assertRaises(RepoError):
            extract_index_text(b"not an archive")

    def test_dependencies(self):
        repo = ApkRepository(parse_index(SAMPLE))
        self.assertEqual(
            repo.dependencies("app"), ["musl", "zlib", "other"]
        )

    def test_unknown_package(self):
        repo = ApkRepository(parse_index(SAMPLE))
        self.assertFalse(repo.has_package("nope"))