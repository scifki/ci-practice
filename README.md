# ci-practice — CI/CD пайплайн для Python-проекта

Учебный репозиторий по практической работе «CI/CD пайплайны» на GitHub Actions.
Проект — небольшая библиотека валидаторов, вокруг которой строится конвейер:
линтер → тесты в двух шардах → карантин нестабильных тестов → тесты в Docker → деплой на staging.

## Структура

```
app/validators.py          проверка e-mail, возраста, нормализация телефона
tests/test_validators.py   7 параметризованных проверок
tests/test_slow.py         8 медленных тестов (для шардирования)
tests/test_flaky.py        нестабильный тест под маркером quarantine
.github/workflows/ci.yml   описание конвейера
Dockerfile                 образ для прогона тестов в контейнере
pytest.ini                 pythonpath и маркер quarantine
requirements.txt           pytest, pytest-split, ruff
```

## Задания и результат

| Задание | Что сделано | Итог |
| --- | --- | --- |
| 1 | Базовый workflow: checkout, Python 3.12, установка зависимостей, pytest | зелёный |
| 2 | Джоба `lint` с `ruff check .` перед тестами | зелёный |
| 3 | Чистая структура проекта: `app/`, `tests/`, `pytest.ini` | зелёный |
| 4 | Разбиение тестов на 2 шарда через `pytest-split` и matrix | зелёный |
| 5 | Карантин нестабильного теста маркером `quarantine` + отдельная джоба `continue-on-error` | зелёный |
| 6 | Сборка Docker-образа и прогон тестов внутри контейнера | зелёный |

Дополнительно: артефакты `junit-report-1.xml` и `junit-report-2.xml` выгружаются
через `actions/upload-artifact`, а джоба `deploy-staging` запускается только для ветки `main`
и только после успешных `unit` и `docker-tests`.

## Схема конвейера

```
lint ──┬── unit (shard 1) ──┐
       └── unit (shard 2) ──┼── deploy-staging (только main)
       └── docker-tests ────┘
quarantine (continue-on-error, не блокирует)
```

## Локальный запуск

```bash
pip install -r requirements.txt
pytest -m "not quarantine" -v
pytest -m quarantine -v
ruff check .
docker build -t ci-practice-tests .
docker run --rm ci-practice-tests
```

## Эксперименты

- Ветка `feature/break-test` с намеренно сломанным тестом: пайплайн упал на джобе `unit`,
  `deploy-staging` не запустился — защита от выкладки сломанной версии работает.
- Коммит `Эксперимент: убрали маркер карантина`: нестабильный тест попал в основной прогон,
  из-за чего сборка стала плавающей. Маркер возвращён, джоба `quarantine` вынесена отдельно.
