"""Визуализация: стандартные графики в dark_background стиле."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # ponytail: headless backend, интерактив не нужен
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use("dark_background")


def plot_hist(df: pd.DataFrame, col: str, out_dir: str | Path = "reports") -> Path:
    """Гистограмма колонки, сохраняет PNG. Возвращает путь к файлу."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"hist_{col}.png"
    df[col].plot.hist()
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    return path


def plot_corr_heatmap(df: pd.DataFrame, out_dir: str | Path = "reports") -> Path:
    """Тепловая карта корреляций, сохраняет PNG. Возвращает путь к файлу."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "corr_heatmap.png"
    corr = df.select_dtypes(include="number").corr()
    plt.imshow(corr, cmap="coolwarm")
    plt.colorbar()
    plt.xticks(range(len(corr)), corr.columns, rotation=45)
    plt.yticks(range(len(corr)), corr.columns)
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    return path
