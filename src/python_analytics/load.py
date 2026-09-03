"""Загрузка данных из CSV в DataFrame."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_csv(path: str | Path, encoding: str = "utf-8") -> pd.DataFrame:
    """Загрузить CSV в DataFrame.

    Args:
        path: путь к CSV-файлу.
        encoding: кодировка файла (по умолчанию utf-8).

    Returns:
        DataFrame с данными.

    Raises:
        FileNotFoundError: файл не существует.
        ValueError: файл пуст или не содержит данных.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Файл не найден: {p}")
    if p.stat().st_size == 0:
        raise ValueError(f"Файл пуст: {p}")
    df = pd.read_csv(p, encoding=encoding)
    if df.empty:
        raise ValueError(f"Файл не содержит данных: {p}")
    return df
