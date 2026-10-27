"""Конфигурация приложения."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """Параметры, заданные пользователем."""

    package: str
    repo: str
    test_mode: bool
    ascii_tree: bool
    filter_substr: str
    reverse: bool