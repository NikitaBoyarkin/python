"""Figures for the `python` EDA report (matplotlib OO style, light theme, PNG 300 dpi).

Produces 5 figures into reports/eda/figures/:
  1. spend distribution (primary metric) with mean/median and negative-value zone
  2. data-quality boxplot: income & spend with negative tails
  3. mean spend by age cohort (derived segment, sorted)
  4. Lorenz / Pareto concentration of spend (lead-finding chart)
  5. correlation matrix (independence check)

Run:
    /Users/nikitaboarkin/Desktop/00 ide/00 portfolio/.eda-tools/.venv/bin/python \
        reports/eda/scripts/plot_figures.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
CSV = ROOT / "data" / "synthetic.csv"
FIG = Path(__file__).resolve().parent.parent / "figures"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "axes.unicode_minus": False,
    }
)

AGE_ORDER = ["18-25", "26-35", "36-50", "51-65", "66+"]


def age_group(a: int) -> str:
    for low, high, label in [
        (18, 25, "18-25"),
        (26, 35, "26-35"),
        (36, 50, "36-50"),
        (51, 65, "51-65"),
        (66, 120, "66+"),
    ]:
        if low <= a <= high:
            return label
    return "other"


def load() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(CSV)
    df = raw.copy()
    num = df.select_dtypes(include="number")
    df[num.columns] = num.fillna(num.median())
    df = df.drop_duplicates().reset_index(drop=True)
    df["age_group"] = df["age"].map(age_group)
    return raw, df


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIG / name, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {FIG / name}")


def fig1_spend_distribution(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 5.5), layout="constrained")
    spend = df["spend"]
    ax.hist(spend, bins=40, color="#4C72B0", edgecolor="white", alpha=0.9)
    mean, median = spend.mean(), spend.median()
    ax.axvline(mean, color="#C44E52", lw=2, label=f"mean = {mean:,.0f}")
    ax.axvline(median, color="#55A868", lw=2, ls="--", label=f"median = {median:,.0f}")
    neg = spend[spend < 0]
    if len(neg):
        ax.axvspan(spend.min(), 0, color="#C44E52", alpha=0.10)
        ax.annotate(
            f"{len(neg)} rows with spend < 0",
            xy=(0, ax.get_ylim()[1] * 0.55),
            xytext=(spend.min(), ax.get_ylim()[1] * 0.8),
            arrowprops=dict(arrowstyle="->", color="#C44E52"),
            color="#C44E52",
            fontsize=10,
        )
    ax.set(
        xlabel="spend",
        ylabel="count",
        title="Distribution of spend (primary metric, n=1000) — near-symmetric, right tail absent",
    )
    ax.legend(frameon=False)
    save(fig, "fig1_spend_distribution.png")


def fig2_quality_boxplot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5.5), layout="constrained")
    data = [df["income"], df["spend"]]
    bp = ax.boxplot(
        data, tick_labels=["income", "spend"], patch_artist=True, widths=0.5
    )
    for patch, color in zip(bp["boxes"], ["#4C72B0", "#DD8452"]):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)
    for median in bp["medians"]:
        median.set_color("black")
    ax.axhline(0, color="#C44E52", lw=1.5, ls="--", label="zero line")
    n_neg = int((df["income"] < 0).sum() + (df["spend"] < 0).sum())
    ax.set(
        xlabel="variable",
        ylabel="value",
        title=f"Monetary variables contain negative values ({n_neg} rows) — validity FAIL",
    )
    ax.legend(frameon=False)
    save(fig, "fig2_quality_boxplot.png")


def fig3_spend_by_age(df: pd.DataFrame) -> None:
    g = (
        df.groupby("age_group", observed=True)["spend"]
        .agg(["mean", "count"])
        .reindex(AGE_ORDER)
    )
    overall = df["spend"].mean()
    fig, ax = plt.subplots(figsize=(9, 5.5), layout="constrained")
    bars = ax.bar(g.index, g["mean"], color="#4C72B0", edgecolor="white")
    ax.axhline(
        overall, color="#C44E52", lw=2, ls="--", label=f"dataset mean = {overall:,.0f}"
    )
    ax.bar_label(
        bars,
        labels=[f"{v:,.0f}  n={int(c)}" for v, c in zip(g["mean"], g["count"])],
        fontsize=9,
        padding=3,
    )
    ax.set_ylim(0, g["mean"].max() * 1.12)
    spread = g["mean"].max() / g["mean"].min()
    ax.set(
        xlabel="age cohort (derived segment)",
        ylabel="mean spend",
        title=f"Mean spend by age cohort — max/min ratio {spread:.2f} (below 1.5 threshold)",
    )
    ax.legend(frameon=False)
    save(fig, "fig3_spend_by_age.png")


def fig4_lorenz(df: pd.DataFrame) -> None:
    v = np.sort(df["spend"].dropna().to_numpy())
    cum = np.cumsum(v)
    cum = np.insert(cum / cum[-1], 0, 0.0)
    x = np.linspace(0.0, 1.0, len(cum))
    n_top = max(1, int(round(len(v) * 0.2)))
    top20 = float(np.sort(v)[::-1][:n_top].sum() / v.sum())
    gini = float((len(v) + 1 - 2 * np.sum(cum[1:]) / cum[-1]) / len(v))

    fig, ax = plt.subplots(figsize=(8, 6), layout="constrained")
    ax.plot(x, cum, color="#4C72B0", lw=2.5, label="Lorenz curve (spend)")
    ax.plot(
        [0, 1],
        [0, 1],
        color="gray",
        ls="--",
        lw=1.5,
        label="perfect equality (20% = 20%)",
    )
    ax.scatter([0.8], [1 - top20], color="#C44E52", zorder=5, s=60)
    ax.annotate(
        f"top 20% hold {top20:.1%} of spend\n(baseline 20% -> only {top20 / 0.20:.2f}x)",
        xy=(0.8, 1 - top20),
        xytext=(0.35, 0.62),
        arrowprops=dict(arrowstyle="->", color="#C44E52"),
        color="#C44E52",
        fontsize=10,
    )
    ax.set(
        xlabel="cumulative share of clients (sorted by spend)",
        ylabel="cumulative share of total spend",
        title=f"Spend concentration is mild — the 'Pareto' label overstates it (Gini {gini:.2f})",
    )
    ax.legend(frameon=False, loc="upper left")
    save(fig, "fig4_lorenz_pareto.png")


def fig5_corr(df: pd.DataFrame) -> None:
    corr = df[["age", "income", "spend"]].corr()
    fig, ax = plt.subplots(figsize=(6.5, 5.5), layout="constrained")
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr)), corr.columns)
    ax.set_yticks(range(len(corr)), corr.columns)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(
                j,
                i,
                f"{corr.iloc[i, j]:.3f}",
                ha="center",
                va="center",
                color="black",
                fontsize=11,
            )
    fig.colorbar(im, ax=ax, label="Pearson r", shrink=0.8)
    ax.set_title("Correlation matrix — all |r| <= 0.054 (independent variables)")
    ax.grid(False)
    save(fig, "fig5_correlation.png")


if __name__ == "__main__":
    _, df = load()
    fig1_spend_distribution(df)
    fig2_quality_boxplot(df)
    fig3_spend_by_age(df)
    fig4_lorenz(df)
    fig5_corr(df)
