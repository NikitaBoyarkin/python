"""Описательная статистика и профилирование данных."""

from __future__ import annotations

import pandas as pd


def describe(df: pd.DataFrame) -> pd.DataFrame:
    """Описательная статистика числовых колонок (mean, median, quantiles)."""
    stats = df.describe().T
    stats["median"] = df.median(numeric_only=True)
    return stats


def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    """Таблица пропусков: колонка, количество, доля. Только колонки с пропусками."""
    missing = df.isna().sum()
    report = pd.DataFrame({"missing": missing, "pct": (missing / len(df)).round(4)})
    return report[report["missing"] > 0]


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Матрица корреляций числовых колонок."""
    return df.select_dtypes(include="number").corr()
