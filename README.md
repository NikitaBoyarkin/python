# Python Analytics Playground

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
