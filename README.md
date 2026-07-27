# 🚀 Download & Analyze File Service

> Сервис для фоновой загрузки файлов из внешнего API, хранения их метаданных, анализа содержимого и отображения прогресса в режиме реального времени.

---

## 📖 О проекте

**Download & Analyze File Service** — это полнофункциональное клиент-серверное приложение, разработанное в качестве pet-проекта для демонстрации навыков проектирования современных backend-сервисов на **FastAPI** и frontend-приложений на **React**.

Проект получает список файлов из внешнего API, скачивает их пакетами, сохраняет на диск, записывает информацию в PostgreSQL, рассчитывает статистику по содержимому файлов и отображает процесс загрузки через **Server-Sent Events (SSE)** без использования polling.

Основной акцент сделан не на количестве функциональности, а на архитектуре приложения, разделении ответственности между слоями и использовании распространённых паттернов проектирования.

---

# ✨ Возможности

## Backend

- Получение списка файлов из внешнего API
- Скачивание файлов пакетами по 3 файла
- Автоматическая распаковка ZIP-архивов
- Сохранение файлов в локальное хранилище
- Хранение метаданных файлов в PostgreSQL
- Повторные попытки запросов (Retry Policy)
- Обработка ошибок `429 Too Many Requests`
- Поддержка заголовка `Retry-After`
- Обработка блокировки (`403 Forbidden`)
- Фоновая загрузка файлов (`asyncio.create_task`)
- Защита от повторного запуска загрузки
- Передача прогресса загрузки через SSE
- Кэширование статистики файлов в базе данных

---

## Frontend

- Запуск загрузки одной кнопкой
- Отображение текущего прогресса
- Обновление интерфейса в режиме реального времени
- Таблица скачанных файлов
- Пагинация
- Выделение отдельных файлов
- Выделение страницы
- Выделение всех файлов
- Просмотр статистики выбранных файлов

---

# 🏗 Архитектура

Проект построен по классической многослойной архитектуре.

```
React
    │
REST API + SSE
    │
FastAPI
    │
────────────────────────────────────
│             │                    │
DownloadService  StatisticsService  FilesService
        │
ExternalApiClient
        │
RetryPolicy
        │
Unit Of Work
        │
Repositories
        │
SQLAlchemy
        │
PostgreSQL
```

Каждый слой отвечает только за свою область ответственности.

---

# 📂 Структура проекта

```
Download-And-Analyze-File-Service
│
├── backend
│   │
│   ├── alembic
│   │
│   ├── app
│   │   │
│   │   ├── api
│   │   ├── core
│   │   ├── dependencies
│   │   ├── factories
│   │   ├── integrations
│   │   ├── managers
│   │   ├── models
│   │   ├── repositories
│   │   ├── schemas
│   │   ├── services
│   │   ├── storages
│   │   └── unit_of_work
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend
│   │
│   ├── src
│   │   ├── api
│   │   ├── components
│   │   ├── hooks
│   │   ├── pages
│   │   ├── types
│   │   └── App.tsx
│   │
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

---

# ⚙️ Используемые технологии

## Backend

- Python 3.13
- FastAPI
- SQLAlchemy 2.0 (Async ORM)
- Alembic
- PostgreSQL
- Pydantic v2
- HTTPX
- asyncio

---

## Frontend

- React
- TypeScript
- Vite
- React Router
- Server-Sent Events

---

## Infrastructure

- Docker
- Docker Compose

---

# 🧩 Использованные архитектурные решения

В проекте используются следующие паттерны.

## Repository Pattern

Вся работа с базой данных вынесена в репозитории.

```
FileRepository

FileStatisticsRepository
```

Бизнес-логика не зависит от SQLAlchemy.

---

## Unit of Work

Все изменения базы данных проходят через единый UnitOfWork.

Он отвечает за

- открытие сессии
- commit
- rollback
- закрытие соединения

---

## Dependency Injection

Все зависимости создаются через FastAPI Depends.

Это позволяет легко заменять реализации.

---

## Factory

Создание сложных сервисов вынесено в отдельные фабрики.

Например:

```
DownloadServiceFactory
```

---

## Service Layer

Вся бизнес-логика находится в сервисах.

Например

```
DownloadService

StatisticsService
```

API ничего не знает о внутренней реализации.

---

## Background Jobs

Загрузка файлов выполняется в фоне.

```
asyncio.create_task(...)
```

Запрос

```
POST /download
```

возвращается сразу.

---

## SSE (Server-Sent Events)

Для передачи прогресса используется

```
GET /download/events
```

Клиент получает обновления мгновенно без постоянного опроса сервера.

---

## Retry Policy

Вынесена отдельным классом.

Поддерживает

- Retry
- Retry-After
- HTTP 429
- HTTP 403

DownloadService вообще ничего не знает про сетевые ошибки.

---

## Cache

Статистика файла после первого расчета сохраняется в таблицу

```
file_statistics
```

Повторный запрос не читает файл повторно.

---

# 📊 Работа приложения

## 1.

Пользователь нажимает

```
Скачать
```

↓

## 2.

Создается Background Task

↓

## 3.

Получаются имена файлов

↓

## 4.

Файлы скачиваются пакетами

↓

## 5.

ZIP распаковывается

↓

## 6.

Файлы сохраняются

↓

## 7.

Метаданные сохраняются в PostgreSQL

↓

## 8.

SSE отправляет прогресс

↓

## 9.

После выбора файлов рассчитывается статистика

↓

## 10.

Статистика сохраняется в БД

↓

## 11.

При повторном запросе используется кэш

---

# 🚀 Запуск проекта

## Требования

Установлены

- Docker
- Docker Compose

---

## Клонирование

```bash
git clone https://github.com/<username>/Download-And-Analyze-File-Service.git

cd Download-And-Analyze-File-Service
```

---

## Запуск

```bash
docker compose up --build
```

После первого запуска будут автоматически:

- поднята PostgreSQL
- выполнены миграции Alembic
- запущен FastAPI
- запущен React

---

# 🌐 Доступные адреса

## Frontend

```
http://localhost:5173
```

---

## Backend

```
http://localhost:8000
```

---

## Swagger

```
http://localhost:8000/docs
```

---

# 📚 REST API

## Проверка состояния

```
GET /
```

---

## Запуск загрузки

```
POST /download
```

Ответ

```json
{
    "status": "started"
}
```

Если загрузка уже выполняется

```
409 Conflict
```

---

## Получение событий

```
GET /download/events
```

Пример события

```json
{
    "received_names": 15,
    "downloaded_files": 12,
    "total_downloaded": 345
}
```

---

## Получение файлов

```
GET /files?page=1&size=20
```

---

## Получение файла

```
GET /files/{id}
```

---

## Расчет статистики

```
POST /statistics
```

Request

```json
{
    "file_ids": [
        1,
        2,
        3
    ]
}
```

Response

```json
{
    "total": {
        "0": 52,
        "1": 48
    },
    "files": [
        {
            "id": 1,
            "name": "example.txt",
            "statistics": {
                "0": 20,
                "1": 15
            }
        }
    ]
}
```

---

# 📡 SSE

Frontend открывает соединение

```
GET /download/events
```

Во время загрузки сервер отправляет события

```
STARTED

Получено 18 имен

Скачано 3

Скачано 6

Скачано 9

Получено 12 имен

...

FINISHED
```

Это позволяет обновлять интерфейс без polling.

---

# 🗄 База данных

Используются две основные таблицы.

## files

Хранит информацию о скачанных файлах.

| Поле | Тип |
|------|-----|
| id | integer |
| name | varchar |
| path | varchar |
| downloaded_at | timestamp |

---

## file_statistics

Кэш статистики файлов.

| Поле | Тип |
|------|-----|
| file_id | integer |
| counts | JSON |

Пример

```json
{
    "0": 51,
    "1": 48,
    "2": 60,
    "3": 55,
    "4": 49,
    "5": 53,
    "6": 41,
    "7": 52,
    "8": 44,
    "9": 47
}
```

---

# 📷 Скриншоты

После завершения проекта рекомендуется добавить изображения.

```
docs/

└── screenshots

    ├── download.png

    ├── files.png

    ├── statistics.png

    └── swagger.png
```

---

# 🔮 Возможные улучшения

Backend

- Redis для хранения состояния загрузки
- Celery/RQ вместо asyncio
- JWT авторизация
- RBAC
- Prometheus + Grafana
- Структурированное логирование

Frontend

- React Query
- Zustand
- Виртуализация больших таблиц
- Графики статистики
- Темная тема

Infrastructure

- Nginx
- GitHub Actions
- CI/CD
- Kubernetes
- MinIO / Amazon S3 вместо локального хранилища

---

# 🎯 Что демонстрирует проект

Проект демонстрирует практические навыки разработки современных веб-приложений:

- проектирование многослойной архитектуры;
- работа с асинхронным Python;
- использование FastAPI и SQLAlchemy Async;
- применение паттернов Repository, Unit of Work, Factory и Dependency Injection;
- интеграция с внешними HTTP API;
- обработка ошибок и реализация Retry Policy;
- работа с PostgreSQL и Alembic;
- реализация фоновых задач;
- передача событий через Server-Sent Events;
- разработка SPA на React + TypeScript;
- контейнеризация приложения с использованием Docker Compose.

---

# 👨‍💻 Автор

Проект разработан в учебных и демонстрационных целях как пример полнофункционального full-stack приложения с акцентом на архитектуру, расширяемость и использование современных практик разработки.