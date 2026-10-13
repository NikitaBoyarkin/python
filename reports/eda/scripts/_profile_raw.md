# EDA Report

**Rows:** 1005 · **Columns:** 3 · **Memory:** 0.02 MB

## Profile

| Column | dtype |
|---|---|
| age | int64 |
| income | float64 |
| spend | float64 |

## Data Quality

- Duplicated rows: **5**
- Constant columns: **0**

| Column | Nulls | Share |
|---|---:|---:|
| income | 21 | 2.1% |

## Numeric Distributions

| Column | n | mean | median | std | p25 | p75 | p95 | outliers | skew |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| age | 1005 | 43.6368 | 44.0 | 14.9841 | 30.0 | 57.0 | 67.0 | 0.0% | -0.0325 |
| income | 984 | 49597.3557 | 50032.5 | 15334.315 | 39545.815 | 59483.0075 | 74293.8605 | 0.9% | -0.1202 |
| spend | 1005 | 19313.0722 | 19753.34 | 8065.2946 | 13982.71 | 24664.87 | 32388.884 | 1.1% | -0.0157 |

## Categorical Slices

_Категориальных колонок нет._

## Correlations

_Пар с |r| >= 0.5 нет._

## Findings

- **[WARN]** Дубликаты строк: 5 — проверить grain

## What We Did Not Cover

- Причинность: корреляции не доказывают влияние.
- Внешние источники и бизнес-контекст, которых нет в датасете.
- Формальные тесты гипотез (это CDA / A-B testing).

## Reproducibility

```bash
uv run python .claude/skills/eda/scripts/eda_profile.py --input <dataset> \
    [--metric <col>] [--segments <a,b>] [--time-col <col>] [--top <n>]
```
