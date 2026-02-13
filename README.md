# FastAPI Blog Backend

Backend-приложение для блога с админскими CRUD-операциями, публичным API и системой управления пользователями.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.x-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=flat)](https://sqlalchemy.org)
[![Pydantic](https://img.shields.io/badge/Pydantic-V2-9206c1?style=flat&logo=pydantic)](https://docs.pydantic.dev)
[![Tests](https://img.shields.io/badge/tests-23%20passed-brightgreen?style=flat&logo=pytest)](https://docs.pytest.org)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat&logo=docker)](https://docker.com)

---

## Возможности

### **Аутентификация и авторизация**
- Регистрация и вход по email/паролю
- JWT токены (access + refresh)
- Bcrypt — хэширование паролей
- Ролевая модель: **USER** (по умолчанию) и **ADMIN**

### **Контент**
- Публичные посты и категории
- CRUD для постов и категорий (только ADMIN)
- Уникальные slug-идентификаторы
- Санитизация HTML через **Bleach** (защита от XSS)

### **Безопасность**
- HTML очищается от опасных тегов и атрибутов
- Разрешённые теги: `p`, `br`, `strong`, `em`, `ul`, `ol`, `li`, `a`, `h1`-`h4`, `blockquote`, `code`, `pre`
- Разрешённые атрибуты: `href`, `title`, `alt`

### **Тестирование**
- 23 интеграционных теста
- Pytest + httpx
- Изолированная тестовая БД
- Тесты аутентификации, публичного и защищенного API

### **Деплой**
- Готовый Dockerfile + docker-compose
- SQLite
- Alembic миграции

---

## Быстрый старт

### 1. Клонировать репозиторий
```bash
git clone https://github.com/polinajakovleva1/fastapi-blog.git
cd fastapi-blog
```

### 2. Запустить через Docker (рекомендуется)
```bash
# Создать .env из шаблона
# Linux/Mac:
cp .env.example .env
# Windows:
copy .env.example .env
docker-compose up --build
```

### 3. Или локально
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Зависимости
pip install -r requirements.txt

# Миграции
alembic upgrade head

# Запуск
uvicorn src.app.main:app --reload
```

### 4. Открыть документацию
```
http://localhost:8000/docs
```

---

## Использование

### **Создание пользователя с ролью ADMIN**
```bash
# Создать администратора
python -m src.scripts.create_admin
```

---

## API Endpoints

### **Публичные**
| Метод | Endpoint | Описание |
|-------|---------|----------|
| `GET` | `/api/v1/posts` | Все посты |
| `GET` | `/api/v1/posts/{slug}` | Пост по slug |
| `GET` | `/api/v1/categories` | Все категории |
| `GET` | `/api/v1/categories/{slug}/posts` | Посты категории |

### **Аутентификация**
| Метод | Endpoint | Описание |
|-------|---------|----------|
| `POST` | `/api/v1/auth/register` | Регистрация |
| `POST` | `/api/v1/auth/login` | Вход |
| `POST` | `/api/v1/auth/refresh` | Обновить токены |
| `GET` | `/api/v1/users/me` | Текущий пользователь |

### **Закрытые (только ADMIN)**
| Метод | Endpoint | Описание |
|-------|---------|----------|
| `GET` | `/api/v1/admin/users` | Все пользователи |
| `PATCH` | `/api/v1/admin/users/{id}/role` | Сменить роль |
| `CRUD` | `/api/v1/admin/categories` | Управление категориями |
| `CRUD` | `/api/v1/admin/posts` | Управление постами |

---

## Тестирование

```bash
# Все тесты
pytest -v

# Конкретный файл
pytest src/tests/test_auth.py -v

```

**Результат: 23/23 passed**

---

## Docker

```bash
# Сборка и запуск
docker-compose up --build

# Фоновый режим
docker-compose up -d

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f app
```

---

## Структура проекта

```
fastapi-blog/
├── src/
│   ├── app/
│   │   ├── api/          # Роутеры (v1, admin, public)
│   │   ├── core/         # Конфиг, безопасность, зависимости
│   │   ├── crud/         # Бизнес-логика
│   │   ├── models/       # SQLAlchemy модели
│   │   ├── schemas/      # Pydantic схемы
│   │   ├── utils/        # Санитизация HTML
│   │   └── migrations/   # Alembic миграции
│   ├── tests/            # 23 теста
│   └── scripts/          # Вспомогательные скрипты
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── pytest.ini
└── requirements.txt
```

---

## Технологический стек

| Компонент | Технология |
|----------|------------|
| **Язык** | Python 3.12+ |
| **Фреймворк** | FastAPI + Uvicorn |
| **База данных** | SQLite / PostgreSQL |
| **ORM** | SQLAlchemy 2.0 |
| **Миграции** | Alembic |
| **Валидация** | Pydantic V2 |
| **Аутентификация** | JWT (access/refresh), bcrypt |
| **Санитизация** | Bleach |
| **Тесты** | Pytest + httpx |
| **Контейнеризация** | Docker + docker-compose |

---

## Статус проекта

- [x] 23/23 тестов проходят
- [x] Документация в `/docs`
- [x] Docker-образ готов
- [x] CI/CD-ready


