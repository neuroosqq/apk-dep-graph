"""Построение и показ изображения графа с помощью утилиты d2."""
import shutil
import subprocess
import webbrowser
from pathlib import Path

from src.errors import RenderError

D2_BINARY = "d2"
RENDER_TIMEOUT = 120


def render_image(d2_file, image):
    """Вызвать d2: преобразовать текст диаграммы в изображение."""
    if shutil.which(D2_BINARY) is None:
        raise RenderError("утилита d2 не найдена в PATH (см. d2lang.com)")
    try:
        subprocess.run(
            [D2_BINARY, d2_file, image],
            check=True, capture_output=True, text=True,
            timeout=RENDER_TIMEOUT,
        )
    except (subprocess.SubprocessError, OSError) as error:
        raise RenderError(f"ошибка d2: {error}") from error


def show_image(image):
    """Открыть изображение в браузере по умолчанию."""
    webbrowser.open(Path(image).resolve().as_uri())