"""Тесты разбора параметров командной строки."""
import os
import tempfile
import unittest

from src.cli import parse_config
from src.errors import ConfigError

URL = "https://example.org/alpine/main/x86_64"


class ParseConfigTest(unittest.TestCase):
    """Проверка параметров и ошибок."""

    def test_valid_url_mode(self):
        config = parse_config(["-p", "bash", "-r", URL])
        self.assertEqual(config.package, "bash")
        self.assertFalse(config.test_mode)

    def test_invalid_url(self):
        with self.assertRaises(ConfigError):
            parse_config(["-p", "bash", "-r", "not-a-url"])

    def test_missing_test_file(self):
        with self.assertRaises(ConfigError):
            parse_config(["-p", "A", "-r", "no_such.txt", "-t"])

    def test_lowercase_name_in_test_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "repo.txt")
            with open(path, "w", encoding="utf-8"):
                pass
            with self.assertRaises(ConfigError):
                parse_config(["-p", "a", "-r", path, "-t"])

    def test_filter_inside_package_name(self):
        with self.assertRaises(ConfigError):
            parse_config(["-p", "bash", "-r", URL, "-f", "as"])

    def test_package_is_required(self):
        with self.assertRaises(SystemExit):
            parse_config(["-r", URL])