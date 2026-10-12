# Python Analytics Playground

> Пайплайн Python-аналитики (загрузка → очистка → EDA → визуализация) на синтетике seed=42; **34 теста** и порог покрытия **≥80 %**.

## Навигация
- 🌐 [Портфолио](https://nikitaboyarkin.github.io)
- 🏦 [Флагманский кейс: Volta neobank](https://github.com/NikitaBoyarkin/volta-banking)
- 🧪 Связанные: [rfm-analysis-of-bank-clients](https://github.com/NikitaBoyarkin/rfm-analysis-of-bank-clients) · [sql-analytics-case-study](https://github.com/NikitaBoyarkin/sql-analytics-case-study) · [churn-prediction](https://github.com/NikitaBoyarkin/churn-prediction)

**На этой странице:** [Ситуация](#ситуация) · [Задача](#задача) · [Действия](#действия) · [Результат](#результат) · [Структура](#структура) · [Запуск](#запуск) · [Пример](#пример) · [PRD](#prd)

## Ситуация

Аналитическому портфолио нужен воспроизводимый каркас, а не набор разрозненных
скриптов: одно место, где загрузка, очистка, разведочный анализ и графики
собраны в повторяемый пайплайн и покрыты тестами.

## Задача

Собрать модульный пакет `python_analytics` со сквозным пайплайном и держать
покрытие тестами на уровне **≥80 %** (`pyproject.toml`).

## Действия

- Загрузка и очистка — `load_csv`, `clean_missing(strategy="fill")`, `deduplicate` (`src/python_analytics/load.py`, `clean.py`).
- EDA — `describe`, `missing_report`, `correlation_matrix` (`src/python_analytics/eda.py`).
- Визуализация — `plot_hist`, `plot_corr_heatmap` (`src/python_analytics/viz.py`).
- Сквозной пайплайн — `run_pipeline()` генерирует синтетику, чистит, считает EDA и рисует графики (`src/python_analytics/pipeline.py:30`).
- Отчёты в Markdown — `generate_report` (`report.py`) и `segmentation_report` (`segment.py`).
- Сегментация — возрастные когорты, `value_segments` (квартили по `spend`), `high_value_share` — правило Парето (`src/python_analytics/segment.py`).

## Результат

- **34 теста** — `tests/` (7 clean + 4 eda + 4 load + 2 pipeline + 1 report + 14 segment + 2 viz).
- **≥ 80 %** — порог покрытия `--cov-fail-under=80` (`pyproject.toml`).
- **1 000 строк** — синтетика по умолчанию: `generate_synthetic_data(n=1000, seed=42)` + 5 дубликатов и 20 пропусков в `income` (`pipeline.py:16`).
- **2 отчёта** — `reports/report.md` и `reports/segmentation_report.md`.

Аналитический портфолио-проект: модули загрузки, очистки, EDA и визуализации данных. Покрытие тестами ≥80%.

## Структура

```
src/python_analytics/
├── load.py       # загрузка CSV (REQ-002)
├── clean.py      # пропуски, дубликаты, типы (REQ-003)
├── eda.py        # статистика, пропуски, корреляции (REQ-004)
├── viz.py        # гистограммы, тепловые карты (REQ-005)
└── pipeline.py   # end-to-end пайплайн (REQ-006)
```

`input.py`, `print.py`, `variables.py` — ранние учебные скрипты, сохранены для истории.

## Запуск

```bash
uv sync --all-groups
uv run pytest                          # тесты + покрытие (≥80%)
uv run python -m python_analytics      # end-to-end пайплайн
```

## Пример

```python
from python_analytics.load import load_csv
from python_analytics.clean import clean_missing, deduplicate

df = load_csv("data/synthetic.csv")
df = clean_missing(df, strategy="fill")
df = deduplicate(df)
```

## PRD

Полный PRD: `docs/prd.md`. Vault-заметка: `PRD - Python Analytics Playground` (Obsidian, Z-core).
