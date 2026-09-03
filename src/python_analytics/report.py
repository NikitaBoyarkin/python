"""Генерация отчёта анализа в Markdown."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from python_analytics.eda import correlation_matrix, describe, missing_report
from python_analytics.viz import plot_corr_heatmap, plot_hist


def _to_markdown(df: pd.DataFrame) -> str:
    """DataFrame → markdown-таблица (без зависимости от tabulate)."""
    cols = list(df.columns)
    header = "| " + " | ".join(cols) + " |"
    sep = "|" + "|".join(["---"] * len(cols)) + "|"
    rows = []
    for idx, row in df.iterrows():
        rows.append("| " + " | ".join([str(idx)] + [str(v) for v in row]) + " |")
    return "\n".join([header, sep] + rows)


def generate_report(
    df: pd.DataFrame,
    out_dir: str | Path = "reports",
    hist_col: str | None = None,
) -> Path:
    """Создать Markdown-отчёт со статистикой и графиками. Возвращает путь к файлу.

    Args:
        df: данные для отчёта.
        out_dir: куда сохранить отчёт и графики.
        hist_col: колонка для гистограммы; по умолчанию первая числовая.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    if hist_col is None:
        numeric = df.select_dtypes(include="number").columns
        hist_col = numeric[0] if len(numeric) else None

    stats = describe(df)
    missing = missing_report(df)
    corr = correlation_matrix(df)
    heatmap_path = plot_corr_heatmap(df, out)
    hist_path = plot_hist(df, hist_col, out) if hist_col else None

    lines = [
        "# Отчёт анализа",
        "",
        f"- Строк: {len(df)}, колонок: {len(df.columns)}",
        "",
        "## Статистика",
        "",
        _to_markdown(stats),
        "",
        "## Пропуски",
        "",
        _to_markdown(missing) if not missing.empty else "нет",
        "",
        "## Корреляции",
        "",
        _to_markdown(corr),
        "",
        "## Графики",
        "",
    ]
    if hist_path:
        lines += [f"![Гистограмма]({hist_path.name})", ""]
    lines += [f"![Тепловая карта]({heatmap_path.name})", ""]

    path = out / "report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
