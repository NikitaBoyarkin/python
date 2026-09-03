"""Очистка данных: пропуски, дубликаты, типы."""

from __future__ import annotations

import pandas as pd


def clean_missing(df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
    """Обработать пропуски.

    Args:
        df: исходный DataFrame.
        strategy: "drop" — удалить строки с NaN, "fill" — заполнить медианой.

    Returns:
        Новый DataFrame без мутации исходного.

    Raises:
        ValueError: неизвестная стратегия.
    """
    result = df.copy()
    if strategy == "drop":
        return result.dropna()
    if strategy == "fill":
        numeric = result.select_dtypes(include="number")
        result[numeric.columns] = numeric.fillna(numeric.median())
        return result
    raise ValueError(f"Неизвестная стратегия: {strategy!r}. Ожидается 'drop' или 'fill'.")


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """Удалить дубликаты строк. Возвращает новый DataFrame."""
    return df.copy().drop_duplicates()


def coerce_types(df: pd.DataFrame, schema: dict[str, str]) -> pd.DataFrame:
    """Привести типы колонок по схеме {колонка: dtype}.

    Args:
        df: исходный DataFrame.
        schema: например {"age": "int64", "price": "float64"}.

    Returns:
        Новый DataFrame с приведёнными типами.

    Raises:
        KeyError: колонка из схемы отсутствует в DataFrame.
    """
    result = df.copy()
    for col, dtype in schema.items():
        if col not in result.columns:
            raise KeyError(f"Колонка не найдена: {col}")
        result[col] = result[col].astype(dtype)
    return result
