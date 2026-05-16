# 📚 Library Catalog API

REST API для управления библиотечным каталогом, построенный на FastAPI с многослойной архитектурой.

## 🚀 Возможности

- CRUD операции с книгами
- Поиск и фильтрация по названию, автору, жанру, доступности
- Пагинация результатов
- Автоматическое обогащение данных из [Open Library](https://openlibrary.org/developers/api)
- Хранение данных в PostgreSQL
- Async/await на всех уровнях
- Автодокументация (Swagger UI / ReDoc)

## 🛠️ Технологии

| Компонент     | Технология   | Версия  |
|---------------|--------------|---------|
| Web Framework | FastAPI       | 0.109+  |
| ASGI Server   | Uvicorn       | 0.27+   |
| Database      | PostgreSQL    | 16+     |
| ORM           | SQLAlchemy    | 2.0+    |
| Migrations    | Alembic       | 1.13+   |
| Validation    | Pydantic      | 2.5+    |
| HTTP Client   | httpx         | 0.26+   |
| Package Mgmt  | Poetry        | latest  |

## 📁 Структура проекта

```
library_catalog/
├── src/
│   └── library_catalog/
│       ├── main.py               # Точка входа
│       ├── api/                  # API Layer: роутеры, схемы, зависимости
│       ├── core/                 # Конфиг, БД, логирование, исключения
│       ├── data/                 # Data Layer: модели, репозитории
│       ├── domain/               # Domain Layer: сервисы, маперы
│       └── external/             # External Layer: клиенты внешних API
├── alembic/                      # Миграции БД
├── tests/                        # Unit и интеграционные тесты
├── docker-compose.yml
├── pyproject.toml
└── .env.example
```

## ⚙️ Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone <repo-url>
cd library_catalog
```

### 2. Установить зависимости

```bash
poetry install
```

### 3. Настроить переменные окружения

```bash
cp .env.example .env
# Отредактировать .env под свои параметры
```

### 4. Запустить PostgreSQL через Docker

```bash
docker-compose up -d
```

### 5. Применить миграции

```bash
poetry run alembic upgrade head
```

### 6. Запустить приложение

```bash
poetry run uvicorn src.library_catalog.main:app --reload
```

Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

## 📖 Документация API

| URL | Описание |
|-----|----------|
| [/docs](http://localhost:8000/docs) | Swagger UI |
| [/redoc](http://localhost:8000/redoc) | ReDoc |
| [/api/v1/health](http://localhost:8000/api/v1/health) | Health check |

## 🔌 Эндпоинты

### Книги

| Метод  | URL                      | Описание                          |
|--------|--------------------------|-----------------------------------|
| POST   | `/api/v1/books/`         | Создать книгу                     |
| GET    | `/api/v1/books/`         | Список книг (с фильтрами)         |
| GET    | `/api/v1/books/{id}`     | Получить книгу по ID              |
| PATCH  | `/api/v1/books/{id}`     | Обновить книгу                    |
| DELETE | `/api/v1/books/{id}`     | Удалить книгу                     |

### Параметры фильтрации (GET `/api/v1/books/`)

| Параметр    | Тип     | Описание                              |
|-------------|---------|---------------------------------------|
| `title`     | string  | Поиск по названию (частичное совпадение) |
| `author`    | string  | Поиск по автору                       |
| `genre`     | string  | Фильтр по жанру                       |
| `available` | boolean | Фильтр по доступности                 |
| `limit`     | int     | Размер страницы (по умолчанию: 20)    |
| `offset`    | int     | Смещение (по умолчанию: 0)            |

## 🏗️ Архитектура

Приложение построено на принципах многослойной архитектуры:

```
API Layer → Domain Layer → Data Layer
                       ↘ External Layer
```

- **API Layer** — принимает HTTP-запросы, валидирует данные, возвращает ответы. Без бизнес-логики.
- **Domain Layer** — вся бизнес-логика: валидация правил, координация репозиториев и внешних клиентов.
- **Data Layer** — CRUD-операции с PostgreSQL через SQLAlchemy.
- **External Layer** — HTTP-клиенты для внешних API (Open Library).

## 🧪 Тесты

```bash
# Все тесты
poetry run pytest

# Только unit-тесты
poetry run pytest tests/unit/

# Только интеграционные тесты
poetry run pytest tests/integration/

# С отчётом о покрытии
poetry run pytest --cov=src/library_catalog
```

## 🗄️ Миграции

```bash
# Создать новую миграцию
poetry run alembic revision --autogenerate -m "описание изменений"

# Применить все миграции
poetry run alembic upgrade head

# Откатить последнюю миграцию
poetry run alembic downgrade -1
```

## 🌍 Переменные окружения

Все переменные описаны в `.env.example`:

| Переменная           | Описание                        | Пример                                          |
|----------------------|---------------------------------|-------------------------------------------------|
| `DATABASE_URL`       | URL подключения к PostgreSQL    | `postgresql+asyncpg://user:pass@localhost/db`   |
| `DEBUG`              | Режим отладки                   | `false`                                         |
| `OPEN_LIBRARY_URL`   | Base URL Open Library API       | `https://openlibrary.org`                       |
| `API_TIMEOUT`        | Таймаут HTTP-запросов (сек)     | `10`                                            |

## 📝 Пример использования

### Создать книгу

```bash
curl -X POST http://localhost:8000/api/v1/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Pragmatic Programmer",
    "author": "David Thomas",
    "year": 2019,
    "genre": "programming",
    "pages": 352,
    "isbn": "9780135957059",
    "available": true
  }'
```

### Получить список книг с фильтром

```bash
curl "http://localhost:8000/api/v1/books/?author=Thomas&available=true&limit=10"
```

## 🤝 Разработка

Проект следует стандартам:
- Именование файлов: `snake_case`
- Именование классов: `PascalCase`
- Именование функций и переменных: `snake_case`
- Константы: `UPPER_CASE`
- Один файл = одна зона ответственности