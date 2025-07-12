# Movies FastAPI Demo

Это демонстрационный REST API для управления коллекцией фильмов, созданный с использованием FastAPI. Проект служит
примером построения асинхронного веб-сервиса на Python с применением современных инструментов для разработки,
тестирования и контроля качества кода.

**Важно:**
В качестве базы данных используется Redis

### 🛠 Стек технологий, статус и качество кода

[![Python Checks](https://github.com/BulatKayrov/movies-fastapi/actions/workflows/python-checks.yaml/badge.svg)](https://github.com/BulatKayrov/movies-fastapi/actions/workflows/python-checks.yaml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![tested with pytest](https://img.shields.io/badge/tested%20with-pytest-00A496.svg?logo=pytest)](https://pytest.org)
[![Python](https://img.shields.io/badge/Python-^3.11-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-44A542?logo=python&logoColor=white)](https://www.uvicorn.org/)

## 🚀 Основные возможности

- **Полный CRUD**: Реализованы все основные операции (Create, Read, Update, Delete) для фильмов.
- **Асинхронность**: API полностью асинхронный благодаря FastAPI и Uvicorn.
- **Валидация данных**: Строгая типизация и валидация запросов и ответов с помощью Pydantic.
- **Тестирование**: Покрытие кода тестами с использованием `pytest`.
- **Автоматическая документация**: Интерактивная документация API доступна "из коробки" (Swagger UI и ReDoc).

## 🔀 API Эндпоинты

| Метод HTTP | Путь                 | Описание                      |
|:-----------|:---------------------|:------------------------------|
| `GET`      | `/movies`            | Получить список всех фильмов. |
| `GET`      | `/movies/{movie_id}` | Получить фильм по его ID.     |
| `POST`     | `/movies`            | Добавить новый фильм.         |
| `PUT`      | `/movies/{movie_id}` | Обновить информацию о фильме. |
| `DELETE`   | `/movies/{movie_id}` | Удалить фильм по его ID.      |

## ⚙️ Установка и запуск

Для запуска проекта на локальной машине выполните следующие шаги.

**1. Клонируйте репозиторий:**

```bash
    git clone https://github.com/BulatKayrov/movies-fastapi.git
    cd movies-fastapi
```

**2. Установите `uv` (если он еще не установлен):**

```bash
# Для macOS / Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh

# Для Windows
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**3. Создайте виртуальное окружение и установите зависимости:**

Команда `sync` установит все основные и dev-зависимости из файла `uv.lock`. `uv` автоматически создаст и активирует
виртуальное окружение в папке `.venv`.

```bash
    uv sync --dev
```

**4. Запуск Redis**

```bash
    docker compose up redis-movie -d
```

**5. Запустите веб-сервер:**

Uvicorn запустит приложение. Флаг `--reload` обеспечит автоматический перезапуск сервера при изменении кода.

```bash
    uvicorn movie_app.main:app --reload
```

После успешного запуска сервер будет доступен по адресу `http://127.0.0.1:8000`.

## 🧪 Запуск тестов

В проекте настроены тесты для проверки корректной работы всех эндпоинтов. Для их запуска выполните команду:

```bash
    cd movie-app/
```

```bash
    pytest
```

Эта команда найдёт и запустит все тесты в файле `movie_app/test_main.py`.

## 📚 Интерактивная документация API

FastAPI автоматически генерирует документацию для всех эндпоинтов. После запуска сервера она доступна по следующим
адресам:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🔄 CI (Непрерывная интеграция)

В репозитории настроен GitHub Actions (`.github/workflows/python-checks.yaml`), который автоматически запускается при
каждом `push` или `pull request` в ветки `main` и `master`.

Пайплайн выполняет следующие проверки:

1. **Форматирование кода**: Проверяет, что весь код отформатирован с помощью `black`.
2. **Линтинг**: Проверяет код на наличие ошибок и стилистических проблем с помощью `ruff`.
