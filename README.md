# File Downloader Service

Сервис для автоматической загрузки файлов из внешнего API, их сохранения, анализа содержимого и отображения прогресса загрузки в реальном времени.

Проект состоит из:

- Backend на FastAPI
- Frontend на React + TypeScript
- PostgreSQL для хранения метаданных
- Docker Compose для запуска всей инфраструктуры


---

# Возможности

## Загрузка файлов

Сервис умеет:

- получать список доступных файлов из внешнего API;
- скачивать файлы пакетами по 3 файла;
- распаковывать ZIP-архивы;
- сохранять файлы в локальное хранилище;
- сохранять информацию о файлах в PostgreSQL;
- отмечать скачанные файлы во внешнем API.


## Фоновая загрузка

Запуск загрузки происходит через API:

```
POST /download
```

Запрос не ожидает завершения загрузки.

После запуска:

- создается background task;
- процесс загрузки выполняется независимо;
- повторный запуск блокируется, если загрузка уже идет.


## Real-time прогресс через SSE

Для обновления состояния используется Server-Sent Events.

Frontend подключается к:

```
GET /download/events
```

И получает события:

```
STARTED

Получено 9 имен

Скачано 3

Скачано 6

Скачано 9

Получено 5 имен

...

FINISHED
```


В отличие от polling, клиент получает изменения сразу после их появления.


## Работа с файлами

Доступны:

Получение списка файлов:

```
GET /files
```

Поддерживается:

- пагинация;
- сортировка по дате загрузки;
- получение количества файлов.


Получение файла:

```
GET /files/{id}
```


## Анализ статистики

Сервис анализирует содержимое файлов и считает количество цифр:

```
0
1
2
...
9
```

Поддерживается:

- общая статистика;
- статистика по каждому файлу;
- кеширование результатов в PostgreSQL.


---

# Архитектура проекта


```
                    React
                      |
                      |
              REST API + SSE
                      |
                      |
                   FastAPI
                      |
        --------------------------------
        |                              |
 DownloadService              StatisticsService
        |                              |
 ExternalApiClient              FileStorage
        |
 RetryPolicy

        |
        |
   Unit Of Work
        |
        |
 Repository Layer
        |
        |
   PostgreSQL


        |
        |
 Local Storage
 /storage/files
```


---

# Backend архитектура


Используются следующие паттерны:

## Repository Pattern

Работа с базой данных вынесена в отдельные репозитории:

```
repositories/

├── file_repository.py
└── file_statistics_repository.py
```


Бизнес-логика не зависит от SQL.


---

## Unit Of Work

Все операции с базой выполняются через:

```
UnitOfWork
```

Он отвечает за:

- создание сессии;
- commit;
- rollback;
- закрытие соединения.


---

## Dependency Injection

FastAPI зависимости используются для создания:

- Database;
- UnitOfWork;
- сервисов;
- клиентов внешнего API.


---

# Стек технологий


## Backend

- Python 3.13
- FastAPI
- SQLAlchemy 2 Async
- PostgreSQL 17
- Alembic
- Pydantic
- httpx
- Docker


## Frontend

- React
- TypeScript
- Vite
- React Router
- Server-Sent Events


## Infrastructure

- Docker Compose
- PostgreSQL container


---

# Структура проекта


```
Download-And-Analyze-File-Service

├── backend
│
│   ├── app
│   │
│   │   ├── api
│   │   │
│   │   ├── services
│   │   │
│   │   ├── repositories
│   │   │
│   │   ├── integrations
│   │   │
│   │   ├── storages
│   │   │
│   │   ├── schemas
│   │   │
│   │   └── unit_of_work
│   │
│   ├── alembic
│   │
│   ├── Dockerfile
│   │
│   └── requirements.txt
│
│
├── frontend
│
│   ├── src
│   │
│   ├── Dockerfile
│   │
│   └── package.json
│
│
├── docker-compose.yml
│
└── README.md
```


---

# Запуск проекта


## Требования

Необходимо установить:

- Docker
- Docker Compose


---

## Запуск


В корне проекта выполнить:


```bash
docker compose up --build
```


Будут запущены:

- PostgreSQL
- FastAPI backend
- React frontend


---

# Адреса приложения


Backend:

```
http://localhost:8000
```


Swagger документация:

```
http://localhost:8000/docs
```


Frontend:

```
http://localhost:5173
```


---

# API


## Health check


```
GET /
```


Ответ:

```json
{
  "status": "ok",
  "service": "File Downloader API"
}
```


---

# Download API


## Запуск загрузки


```
POST /download
```


Ответ:


```json
{
  "status": "started"
}
```


Если загрузка уже выполняется:


```
409 Conflict
```


---

## SSE события загрузки


```
GET /download/events
```


Пример события:


```json
{
  "received_names": 9,
  "downloaded_files": 9,
  "total_downloaded": 9
}
```


---

# Files API


## Получение списка файлов


```
GET /files?page=1&size=20
```


Пример ответа:


```json
{
  "items": [
    {
      "id":1,
      "name":"example.txt",
      "path":"storage/files/example.txt",
      "downloaded_at":"2026-07-26T10:00:00"
    }
  ],
  "total":565
}
```


---

## Получение файла


```
GET /files/{id}
```


---

# Statistics API


Расчет статистики:


```
POST /statistics
```


Request:


```json
{
  "file_ids":[1,2,3]
}
```


Ответ:


```json
{
  "total":{
    "0":150,
    "1":120,
    "2":90
  },
  "files":[
    {
      "id":1,
      "name":"example.txt",
      "statistics":{
        "0":50,
        "1":40
      }
    }
  ]
}
```


---

# Кеширование статистики


После первого расчета:

1. файл читается из storage;
2. считается статистика;
3. результат сохраняется в таблицу:

```
file_statistics
```


При повторном запросе:

```
File
 |
 |
 PostgreSQL
 |
 |
 JSON статистика
```


Файл повторно не читается.


---

# Работа с внешним API


Вся интеграция находится в:


```
app/integrations/external_api
```


Ответственность:

## ExternalApiClient

Работает с HTTP:


- получение имен файлов;
- скачивание архивов;
- подтверждение загрузки.


## RetryPolicy

Обрабатывает:

- повторные запросы;
- задержки;
- HTTP 429;
- Retry-After;
- блокировки 403.


Сервисы приложения не знают о сетевых ошибках.

---

# Возможные улучшения


## Backend

- Redis для хранения состояния загрузки;
- Celery/RQ для очередей;
- JWT авторизация;
- ограничения доступа;
- Prometheus метрики;
- структурированные логи.


## Storage

Вместо локальной папки:

```
/storage/files
```

можно использовать:

- Amazon S3;
- MinIO;
- Azure Blob Storage.


## Database

Возможные улучшения:

- PostgreSQL JSONB вместо JSON;
- дополнительные индексы;
- оптимизация больших объемов данных.


## Frontend

Можно добавить:

- React Query;
- Zustand;
- виртуализацию таблиц;
- графики статистики.


## Infrastructure

Возможные улучшения:

- CI/CD;
- GitHub Actions;
- Nginx;
- Kubernetes deployment.


---

# Проверка работы


После запуска проверить:


## Backend

```
http://localhost:8000/docs
```


## Frontend

```
http://localhost:5173
```


Проверить:


✅ контейнеры запускаются

✅ миграции применяются

✅ загрузка запускается

✅ SSE обновляет прогресс

✅ файлы появляются в storage

✅ данные сохраняются в PostgreSQL

✅ статистика кешируется


---

# Автор


Проект создан как пример полноценного backend/frontend приложения с использованием:

- FastAPI
- React
- PostgreSQL
- Docker
- Async Python