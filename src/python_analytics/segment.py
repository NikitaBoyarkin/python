"""Сегментация клиентов: возрастные когорты, value-сегменты, склонность к тратам.

Данные cross-sectional (страница = клиент), поэтому классический RFM
(recency/frequency/monetary) неприменим — нет истории транзакций. Здесь
используется value-подход: monetary = spend, плюс age-когорты как proxy
для когортного анализа и spend_rate (доля дохода на траты).
"""

from __future__ import annotations

import pandas as pd

from python_analytics.report import _to_markdown

# Границы возрастных когорт: (нижняя, верхняя, метка).
AGE_BUCKETS = [
    (18, 25, "18-25"),
    (26, 35, "26-35"),
    (36, 50, "36-50"),
    (51, 65, "51-65"),
    (66, 120, "66+"),
]

VALUE_LABELS = ["Low", "Medium-Low", "Medium-High", "High"]


def age_group(age: int) -> str:
    """Возраст → метка когорты. Вне диапазона → 'other'."""
    for low, high, label in AGE_BUCKETS:
        if low <= age <= high:
            return label
    return "other"


def assign_age_group(df: pd.DataFrame, age_col: str = "age") -> pd.Series:
    """Категориальная колонка age_group. Не мутирует вход."""
    return pd.Series([age_group(a) for a in df[age_col]], index=df.index, name="age_group")


def spend_rate(df: pd.DataFrame, spend_col: str = "spend", income_col: str = "income") -> pd.Series:
    """Доля дохода, потраченная на spend = spend / income. Ноль/NaN в income → NaN."""
    income = df[income_col].where(df[income_col] != 0)
    rate = df[spend_col] / income
    return rate.round(4).rename("spend_rate")


def value_segments(
    df: pd.DataFrame,
    spend_col: str = "spend",
    n: int = 4,
    labels: list[str] | None = None,
) -> pd.Series:
    """Квартильные сегменты по spend (qcut). Падение на вырожденных данных → равные диапазоны.

    Returns:
        Категориальная колонка с метками сегментов; NaN для строк с NaN в spend.
    """
    result_labels = labels or VALUE_LABELS[:n]
    values = df[spend_col].dropna()
    try:
        cuts = pd.qcut(values, q=n, labels=result_labels, duplicates="raise")
    except ValueError:
        # Недостаточно уникальных значений для квантилей — режем по диапазону.
        cuts = pd.cut(values, bins=n, labels=result_labels)
    return cuts.reindex(df.index).rename("value_seg")


def high_value_share(df: pd.DataFrame, spend_col: str = "spend", top: float = 0.2) -> float:
    """Доля общего spend, которую дают top-{top} клиентов (правило Парето).

    Returns:
        Доля в диапазоне (0, 1].
    """
    values = df[spend_col].dropna().sort_values(ascending=False)
    total = values.sum()
    if total == 0:
        return 0.0
    n_top = max(1, int(round(len(values) * top)))
    return float(values.head(n_top).sum() / total)


def group_summary(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    aggs: tuple[str, ...] = ("mean", "median", "sum"),
) -> pd.DataFrame:
    """Сводка по группе: количество, агрегаты и доля от общей суммы value_col.

    Returns:
        DataFrame с колонками [count, *aggs, share_of_total], отсортированный по count.
    """
    grouped = df.groupby(group_col, observed=True)[value_col]
    summary = grouped.agg(["size", *aggs]).rename(columns={"size": "count"})
    total = summary["sum"].sum() if "sum" in aggs else df[value_col].sum()
    if total:
        summary["share_of_total"] = (summary["sum"] / total).round(4) if "sum" in aggs else pd.NA
    summary = summary.sort_values("count", ascending=False)
    return summary.round(4)


def run_segmentation(df: pd.DataFrame) -> dict[str, pd.DataFrame | float]:
    """Сегментация клиентов одним вызовом.

    Returns:
        dict с ключами: enriched, age_groups, value_segments, spend_rate_by_age, pareto.
    """
    enriched = df.copy()
    enriched["age_group"] = assign_age_group(df)
    enriched["spend_rate"] = spend_rate(df)
    enriched["value_seg"] = value_segments(df)

    return {
        "enriched": enriched,
        "age_groups": group_summary(enriched, "age_group", "spend"),
        "spend_rate_by_age": group_summary(enriched, "age_group", "spend_rate", aggs=("mean", "median")),
        "value_segments": group_summary(enriched, "value_seg", "spend"),
        "pareto": high_value_share(enriched),
    }


def segmentation_report(df: pd.DataFrame, out_dir: str = "reports") -> pd.DataFrame:
    """Записать markdown-отчёт сегментации в out_dir. Возвращает enriched DataFrame."""
    from pathlib import Path  # локальный импорт: не тянуть Path в API пакета

    result = run_segmentation(df)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Отчёт сегментации клиентов",
        "",
        f"- Строк: {len(df)}",
        f"- Pareto: top-20% клиентов дают {result['pareto']:.1%} трат",
        "",
        "## Возрастные когорты",
        "",
        _to_markdown(result["age_groups"]),
        "",
        "## Spend rate по когортам",
        "",
        _to_markdown(result["spend_rate_by_age"]),
        "",
        "## Value-сегменты",
        "",
        _to_markdown(result["value_segments"]),
        "",
    ]
    (out / "segmentation_report.md").write_text("\n".join(lines), encoding="utf-8")
    return result["enriched"]
