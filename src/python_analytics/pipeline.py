"""End-to-end аналитический пайплайн на синтетических данных."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from python_analytics.clean import clean_missing, deduplicate
from python_analytics.eda import correlation_matrix, describe, missing_report
from python_analytics.load import load_csv
from python_analytics.viz import plot_corr_heatmap, plot_hist


def generate_synthetic_data(n: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Сгенерировать синтетический датасет с пропусками и дубликатами."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "age": rng.integers(18, 70, n),
            "income": rng.normal(50000, 15000, n).round(2),
            "spend": rng.normal(20000, 8000, n).round(2),
        }
    )
    df.loc[rng.integers(0, n, 20), "income"] = np.nan
    return pd.concat([df, df.iloc[:5]], ignore_index=True)


def run_pipeline(n: int = 1000, out_dir: str = "reports", data_dir: str = "data") -> dict:
    """Прогнать загрузку → очистку → EDA → визуализацию. Возвращает сводку."""
    data_path = Path(data_dir) / "synthetic.csv"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    generate_synthetic_data(n).to_csv(data_path, index=False)

    df = load_csv(data_path)
    df = clean_missing(df, strategy="fill")
    df = deduplicate(df)

    stats = describe(df)
    missing = missing_report(df)
    corr = correlation_matrix(df)
    hist_path = plot_hist(df, "age", out_dir)
    heatmap_path = plot_corr_heatmap(df, out_dir)

    print("=== EDA отчёт ===")
    print(f"Строк: {len(df)}, колонок: {len(df.columns)}")
    print("\nСтатистика:")
    print(stats[["mean", "median", "std"]].round(2).to_string())
    print("\nПропуски:")
    print(missing.to_string() if not missing.empty else "нет")
    print("\nКорреляции:")
    print(corr.round(2).to_string())
    print(f"\nГрафики: {hist_path}, {heatmap_path}")

    return {"rows": len(df), "hist": str(hist_path), "heatmap": str(heatmap_path)}
