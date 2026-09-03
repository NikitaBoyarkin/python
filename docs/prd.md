# PRD: Python Analytics Playground

**Автор:** Nikita Boyarkin
**Дата:** 2026-09-03
**Статус:** Draft
**Версия:** 1.0

---

## 1. Executive Summary

Папка `00 portfolio/python` сейчас содержит три учебных скрипта по основам Python (`input.py`, `print.py`, `variables.py`) без структуры, тестов и документации. Проект превращается в структурированный аналитический портфолио-проект: модули загрузки, очистки, EDA и визуализации данных с pytest-покрытием ≥80%, uv-пакетированием и публикацией (README + vault-заметка). Ожидаемый эффект — демонстрируемый артефакт аналитических навыков для портфолио и собеседований.

## 2. Problem Statement

### Текущая ситуация
- 3 ad-hoc скрипта (`input`/`print`/`variables`) — базовые упражнения, не аналитика
- Нет структуры пакета, тестов, зависимостей, полноценного README
- Нет данных и аналитических модулей

### Влияние на пользователя
- **Кто затронут:** автор (аналитик), рекрутеры/интервьюеры при просмотре портфолио
- **Как затронут:** папка не демонстрирует аналитические навыки; нет артефакта для портфолио
- **Серьёзность:** Medium — отсутствие структурированного Python-артефакта в портфолио

### Бизнес-влияние
- **Стоимость проблемы:** упущенные офферы/интервью из-за слабого портфолио
- **Стратегическая важность:** портфолио — ключевой актив при поиске работы (см. [[MOC - Career & GitHub Portfolio]])

### Почему решать сейчас
- Активный цикл подготовки к интервью BI/DA (старт 2026-08-08)
- Папка уже существует — минимальный порог для структурирования

## 3. Goals & Success Metrics

### Goal 1: Структурированные аналитические модули
- **Описание:** превратить скретчпад в пакет с модулями загрузки/очистки/EDA/визуализации
- **Метрика:** количество модулей с чёткой ответственностью
- **Baseline:** 0 модулей (3 ad-hoc скрипта)
- **Target:** ≥5 модулей
- **Срок:** 6 недель
- **Метод измерения:** структура репозитория

### Goal 2: Покрытие тестами ≥80%
- **Описание:** pytest-набор для всех модулей
- **Метрика:** % покрытия (coverage.py)
- **Baseline:** 0%
- **Target:** ≥80%
- **Срок:** 6 недель
- **Метод измерения:** `uv run pytest --cov`

### Goal 3: Публикация
- **Описание:** README, vault-заметка, git-история
- **Метрика:** наличие артефактов
- **Baseline:** README = 1 строка
- **Target:** README с описанием, vault-заметка PRD, коммиты
- **Срок:** 6 недель

## 4. User Stories

### Story 1: Демонстрация навыков
**As a** рекрутер/интервьюер, **I want to** увидеть структурированный аналитический проект с тестами, **So that I can** оценить навыки кандидата.

**Acceptance Criteria:**
- [ ] README объясняет цель и структуру проекта
- [ ] Проект запускается одной командой (`uv run`)
- [ ] Тесты проходят (`uv run pytest`)

**Dependencies:** REQ-001, REQ-008

### Story 2: Повторное использование
**As a** автор, **I want to** переиспользовать модули загрузки/очистки в новых задачах, **So that I can** не писать boilerplate заново.

**Acceptance Criteria:**
- [ ] Модули импортируются как пакет
- [ ] Функции документированы (docstrings)
- [ ] Есть примеры использования

**Dependencies:** REQ-002, REQ-003

## 5. Functional Requirements

### Must Have (P0) — критично для запуска

#### REQ-001: Структура пакета (uv + pyproject.toml)
**Описание:** стандартная структура Python-пакета с uv-конфигурацией.

**Acceptance Criteria:**
- [ ] `pyproject.toml` с зависимостями (pandas, matplotlib, numpy, pytest)
- [ ] Пакет импортируется (`import python_analytics`)
- [ ] `uv sync --all-groups` работает без ошибок

**Task Breakdown:**
- Scaffolding: Small (2-4h)
- Конфигурация: Small (2-4h)
- Тесты: Small (2-4h)

**Dependencies:** None

#### REQ-002: Модуль загрузки данных
**Описание:** загрузка CSV/Excel в DataFrame с валидацией.

**Acceptance Criteria:**
- [ ] `load_csv(path)` возвращает DataFrame
- [ ] Несуществующий путь → понятная ошибка
- [ ] Пустой файл → понятная ошибка
- [ ] Поддержка кодировок (utf-8, cp1251)

**Task Breakdown:**
- Загрузка: Small (2-4h)
- Валидация: Small (2-4h)
- Тесты: Small (2-4h)

**Dependencies:** REQ-001

#### REQ-003: Модуль очистки данных
**Описание:** обработка пропусков, дубликатов, типов.

**Acceptance Criteria:**
- [ ] `clean_missing(df, strategy)` обрабатывает NaN
- [ ] `deduplicate(df)` удаляет дубликаты
- [ ] `coerce_types(df, schema)` приводит типы
- [ ] Функции не мутируют входной DataFrame

**Task Breakdown:**
- Очистка: Medium (4-8h)
- Тесты: Medium (4-8h)

**Dependencies:** REQ-002

#### REQ-004: Модуль EDA
**Описание:** описательная статистика и профилирование.

**Acceptance Criteria:**
- [ ] `describe(df)` возвращает статистику (mean, median, quantiles)
- [ ] `missing_report(df)` возвращает таблицу пропусков
- [ ] `correlation_matrix(df)` для числовых колонок
- [ ] Результаты возвращаются как DataFrame

**Task Breakdown:**
- EDA: Medium (4-8h)
- Тесты: Medium (4-8h)

**Dependencies:** REQ-003

#### REQ-005: Модуль визуализации
**Описание:** стандартные графики (hist, box, scatter, heatmap).

**Acceptance Criteria:**
- [ ] `plot_hist(df, col)` сохраняет PNG
- [ ] `plot_corr_heatmap(df)` сохраняет PNG
- [ ] Графики используют `dark_background` стиль
- [ ] Функции возвращают путь к файлу

**Task Breakdown:**
- Визуализация: Medium (4-8h)
- Тесты: Small (2-4h)

**Dependencies:** REQ-004

#### REQ-006: Пример аналитического пайплайна
**Описание:** end-to-end скрипт на синтетических данных.

**Acceptance Criteria:**
- [ ] Скрипт генерирует синтетический датасет
- [ ] Прогоняет загрузку → очистку → EDA → визуализацию
- [ ] Выводит отчёт в консоль
- [ ] Запускается `uv run python -m python_analytics`

**Task Breakdown:**
- Пайплайн: Medium (4-8h)
- Тесты: Medium (4-8h)

**Dependencies:** REQ-002..005

#### REQ-007: Тестовый набор (pytest ≥80%)
**Описание:** покрытие всех модулей.

**Acceptance Criteria:**
- [ ] `uv run pytest` проходит
- [ ] Покрытие ≥80% (coverage.py)
- [ ] Тесты изолированы (fixtures, tmp_path)
- [ ] Edge cases покрыты (пустые данные, ошибки)

**Task Breakdown:**
- Тесты: Medium (4-8h)

**Dependencies:** REQ-002..006

### Should Have (P1) — важно, но не блокирует

#### REQ-008: README и документация
**Описание:** README с описанием, структурой, примерами.

**Acceptance Criteria:**
- [ ] README описывает цель и структуру
- [ ] Примеры запуска команд
- [ ] Ссылка на vault-заметку PRD

**Dependencies:** REQ-001

### Nice to Have (P2) — будущее улучшение

#### REQ-009: Отчёт в Markdown/HTML
**Описание:** генерация отчёта анализа.

**Acceptance Criteria:**
- [ ] `generate_report(df)` создаёт .md
- [ ] Отчёт включает статистику и графики
- [ ] Путь к отчёту возвращается

**Dependencies:** REQ-006

## 6. Non-Functional Requirements

### Performance
- Обработка датасета 100k строк: < 60s
- Визуализация: < 5s на график

### Security
- Нет секретов в коде (`.env` не коммитится)
- Валидация входных путей

### Scalability
- Датасеты до 1M строк
- Модульность для расширения

### Reliability
- Понятные ошибки на невалидных данных
- Функции не мутируют входные данные

## 7. Technical Considerations

### Архитектура
```
python/
├── pyproject.toml
├── src/python_analytics/
│   ├── __init__.py
│   ├── load.py        # REQ-002
│   ├── clean.py       # REQ-003
│   ├── eda.py         # REQ-004
│   ├── viz.py         # REQ-005
│   └── pipeline.py    # REQ-006
├── tests/
│   ├── test_load.py
│   ├── test_clean.py
│   ├── test_eda.py
│   ├── test_viz.py
│   └── test_pipeline.py
├── data/              # синтетические датасеты
├── reports/           # выходные отчёты
└── README.md
```

### Технологический стек
- **Backend:** Python 3.10+, uv
- **Data:** pandas, numpy
- **Visualization:** matplotlib
- **Testing:** pytest, coverage.py

### Внешние зависимости
1. **pandas/numpy:** обработка данных
2. **matplotlib:** визуализация

### Тестирование
- Unit: ≥80% покрытие
- Integration: end-to-end пайплайн

## 8. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
**Goal:** структура пакета + загрузка/очистка
**Tasks:**
- [ ] Task 1.1: scaffolding + pyproject (REQ-001) — Small (3h)
- [ ] Task 1.2: модуль загрузки (REQ-002) — Small (3h)
- [ ] Task 1.3: модуль очистки (REQ-003) — Medium (5h)
**Validation Checkpoint:** `uv run pytest` зелёный, покрытие ≥60%

### Phase 2: Core Features (Week 3-4)
**Goal:** EDA + визуализация + пайплайн
**Tasks:**
- [ ] Task 2.1: модуль EDA (REQ-004) — Medium (5h)
- [ ] Task 2.2: модуль визуализации (REQ-005) — Medium (5h)
- [ ] Task 2.3: пайплайн (REQ-006) — Medium (6h)
**Validation Checkpoint:** пайплайн запускается end-to-end

### Phase 3: Polish & Deploy (Week 5-6)
**Goal:** тесты ≥80%, README, публикация
**Tasks:**
- [ ] Task 3.1: тестовый набор (REQ-007) — Medium (6h)
- [ ] Task 3.2: README (REQ-008) — Small (3h)
- [ ] Task 3.3: vault-заметка + коммиты — Small (2h)
**Validation Checkpoint:** покрытие ≥80%, README полный

### Зависимости задач
```
Phase 1 → Phase 2 → Phase 3
Critical Path: REQ-001 → REQ-002 → REQ-003 → REQ-004 → REQ-005 → REQ-006 → REQ-007
```

### Оценка усилий
- Phase 1: ~11h
- Phase 2: ~16h
- Phase 3: ~11h
- **Итого:** ~38h (~6 недель solo)
- **Риск-буфер:** +20%

## 9. Out of Scope

1. **ML/модели** — отдельный проект, фокус на аналитике
2. **Web-приложение** — нет потребности
3. **Деплой/CI** — локальный портфолио-проект
4. **Реальные данные** — синтетические для воспроизводимости

## 10. Open Questions & Risks

### Open Questions
#### Q1: Набор данных для примера
- **Статус:** синтетический (smart default)
- **Варианты:** (A) синтетический, (B) публичный датасет (Kaggle)
- **Владелец:** автор
- **Влияние:** Low

### Risks & Mitigation

| Риск | Вероятность | Влияние | Severity | Митигация | Контингенция |
|------|-------------|---------|----------|-----------|--------------|
| Scope creep (ML/web) | Medium | Medium | Medium | Out of scope зафиксирован | Вернуться к REQ-списку |
| Низкое покрытие тестов | Medium | Medium | Medium | TDD-подход | Увеличить время на тесты |
| Синтетические данные нереалистичны | Low | Low | Low | Документировать генерацию | Заменить на публичный датасет |

## 11. Validation Checkpoints

### Checkpoint 1: Конец Phase 1
**Критерии:**
- [ ] `uv run pytest` зелёный
- [ ] Покрытие ≥60%
- [ ] Модули load/clean импортируются
**Если провален:** пересмотреть объём Phase 1

### Checkpoint 2: Конец Phase 2
**Критерии:**
- [ ] Пайплайн запускается end-to-end
- [ ] Графики генерируются
**Если провален:** упростить пайплайн

### Checkpoint 3: Конец Phase 3
**Критерии:**
- [ ] Покрытие ≥80%
- [ ] README полный
- [ ] Vault-заметка создана
**Если провален:** продлить фазу

---

**Конец PRD**

*Шаблон: comprehensive. Для минимального PRD оставить разделы 1-5, 8, 9.*
