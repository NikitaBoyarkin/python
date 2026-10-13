"""EDA analysis for the `python` portfolio project (Python Analytics Playground).

Grain: row = one synthetic client (cross-sectional, no time column).
Metric: `spend`. Derived segments: age cohorts (project logic) and spend quartiles.
Reproduces every headline number used in the report and the README truth check.

Run:
    /Users/nikitaboarkin/Desktop/00 ide/00 portfolio/.eda-tools/.venv/bin/python \
        reports/eda/scripts/analysis.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]  # .../python
CSV = ROOT / "data" / "synthetic.csv"
OUT = Path(__file__).resolve().parent / "_summary.json"

AGE_BUCKETS = [
    (18, 25, "18-25"),
    (26, 35, "26-35"),
    (36, 50, "36-50"),
    (51, 65, "51-65"),
    (66, 120, "66+"),
]
VALUE_LABELS = ["Low", "Medium-Low", "Medium-High", "High"]


def age_group(a: int) -> str:
    for low, high, label in AGE_BUCKETS:
        if low <= a <= high:
            return label
    return "other"


def load_raw() -> pd.DataFrame:
    return pd.read_csv(CSV)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Replicates python_analytics.pipeline: fill numeric NaN with median, then dedup."""
    out = df.copy()
    numeric = out.select_dtypes(include="number")
    out[numeric.columns] = numeric.fillna(numeric.median())
    return out.drop_duplicates().reset_index(drop=True)


def pareto_share(values: pd.Series, top: float) -> float:
    v = values.dropna().sort_values(ascending=False)
    total = v.sum()
    n = max(1, int(round(len(v) * top)))
    return float(v.head(n).sum() / total)


def lorenz(values: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    v = np.sort(values.dropna().to_numpy())
    cum = np.cumsum(v)
    cum = np.insert(cum / cum[-1], 0, 0.0)
    x = np.linspace(0.0, 1.0, len(cum))
    return x, cum


def build() -> dict:
    raw = load_raw()
    df = clean(raw)
    df["age_group"] = df["age"].map(age_group)
    df["spend_rate"] = (df["spend"] / df["income"].where(df["income"] != 0)).round(4)
    df["value_seg"] = pd.qcut(df["spend"], 4, labels=VALUE_LABELS)

    s: dict = {}
    s["raw_rows"] = int(len(raw))
    s["raw_cols"] = int(raw.shape[1])
    s["clean_rows"] = int(len(df))
    s["raw_null_income"] = int(raw["income"].isna().sum())
    s["raw_null_age"] = int(raw["age"].isna().sum())
    s["raw_null_spend"] = int(raw["spend"].isna().sum())
    s["raw_full_dups"] = int(raw.duplicated().sum())
    s["clean_full_dups"] = int(df.duplicated().sum())

    # distributions
    dist = {}
    for c in ["age", "income", "spend"]:
        col = df[c]
        q1, q3 = col.quantile([0.25, 0.75])
        iqr = q3 - q1
        outl = ((col < q1 - 1.5 * iqr) | (col > q3 + 1.5 * iqr)).mean()
        dist[c] = {
            "mean": round(float(col.mean()), 4),
            "median": round(float(col.median()), 4),
            "std": round(float(col.std()), 4),
            "p25": round(float(col.quantile(0.25)), 4),
            "p75": round(float(col.quantile(0.75)), 4),
            "p95": round(float(col.quantile(0.95)), 4),
            "min": round(float(col.min()), 4),
            "max": round(float(col.max()), 4),
            "skew": round(float(col.skew()), 4),
            "outlier_share": round(float(outl), 4),
            "negatives": int((col < 0).sum()),
        }
    s["distributions"] = dist

    # correlations (clean)
    corr = df[["age", "income", "spend"]].corr()
    s["corr"] = {
        f"{a}|{b}": round(float(corr.loc[a, b]), 4) for a in corr for b in corr
    }
    s["max_abs_corr"] = round(
        float(corr.where(~np.eye(len(corr), dtype=bool)).abs().max().max()), 4
    )

    # metric by derived segments
    def seg(col: str, value: str = "spend") -> list[dict]:
        g = df.groupby(col, observed=True)[value].agg(
            ["count", "mean", "median", "sum"]
        )
        g["share_of_total"] = g["sum"] / g["sum"].sum()
        return [
            {
                "segment": str(idx),
                "count": int(r["count"]),
                "mean": round(float(r["mean"]), 4),
                "median": round(float(r["median"]), 4),
                "sum": round(float(r["sum"]), 4),
                "share_of_total": round(float(r["share_of_total"]), 4),
            }
            for idx, r in g.iterrows()
        ]

    s["by_age_group"] = seg("age_group")
    s["by_value_seg"] = seg("value_seg")
    s["spend_rate_by_age"] = [
        {
            "segment": str(i),
            "count": int(r["count"]),
            "mean": round(float(r["mean"]), 4),
            "median": round(float(r["median"]), 4),
        }
        for i, r in df.groupby("age_group", observed=True)["spend_rate"]
        .agg(["count", "mean", "median"])
        .iterrows()
    ]

    # pareto / concentration
    s["pareto_top10"] = round(pareto_share(df["spend"], 0.10), 4)
    s["pareto_top20"] = round(pareto_share(df["spend"], 0.20), 4)
    s["pareto_top30"] = round(pareto_share(df["spend"], 0.30), 4)
    s["gini_spend"] = round(float(gini(df["spend"])), 4)

    # spend_rate quality
    s["spend_rate_mean"] = round(float(df["spend_rate"].mean()), 4)
    s["spend_rate_median"] = round(float(df["spend_rate"].median()), 4)
    s["spend_rate_min"] = round(float(df["spend_rate"].min()), 4)
    s["spend_rate_max"] = round(float(df["spend_rate"].max()), 4)
    s["spend_rate_negative"] = int((df["spend_rate"] < 0).sum())

    # validity
    s["age_in_range"] = bool(((df["age"] >= 0) & (df["age"] <= 120)).all())
    s["income_negative"] = int((df["income"] < 0).sum())
    s["spend_negative"] = int((df["spend"] < 0).sum())
    s["age_min"] = int(df["age"].min())
    s["age_max"] = int(df["age"].max())

    return s


def gini(values: pd.Series) -> float:
    v = np.sort(values.dropna().to_numpy())
    n = len(v)
    cum = np.cumsum(v)
    return float((n + 1 - 2 * np.sum(cum) / cum[-1]) / n)


if __name__ == "__main__":
    summary = build()
    OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\nWrote {OUT}")
