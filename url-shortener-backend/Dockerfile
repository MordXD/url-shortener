# 1. Базовый минимальный образ
FROM python:3.12-slim AS base

# 2. Установка зависимостей системы (чтобы Poetry и Redis работали)
RUN apt-get update && apt-get install -y \
    build-essential curl libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s ~/.local/bin/poetry /usr/local/bin/poetry

# 4. Установка зависимостей через Poetry
WORKDIR /app

# Копируем только зависимости для кэша
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry lock && \
    poetry install --no-interaction --no-ansi

# 5. Копируем сам код проекта
COPY app/ ./app/

# 6. Запускаем сервер FastAPI
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]