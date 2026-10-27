"""Классы ошибок приложения."""


class AppError(Exception):
    """Базовая ошибка приложения."""


class ConfigError(AppError):
    """Ошибка в параметрах, заданных пользователем."""

class RepoError(AppError):
    """Ошибка получения или разбора данных репозитория."""

class RenderError(AppError):
    """Ошибка построения изображения графа."""