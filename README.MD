# URL Shortener

Сервис для сокращения длинных URL-адресов.

## Особенности

- Быстрое создание коротких URL
- Ограничение количества запросов (rate limiting)
- Redis для хранения данных
- Docker-контейнеризация
- Полная документация API

## Запуск проекта

```bash
docker-compose up -d
```

## API Endpoints

### Сокращение URL

```bash
curl -X 'POST' \
  'http://localhost:8000/shorten' \
  -H 'Content-Type: application/json' \
  -d '{
  "original_url": "https://example.com/very/long/url/that/needs/shortening"
}'
```

#### Ответ

```json
{
  "short_url": "http://localhost:8000/AbCdEf"
}
```

### Переход по сокращенному URL

```
GET http://localhost:8000/{short_code}
```

Например:
```
http://localhost:8000/AbCdEf
```

Результат: Редирект на оригинальный URL-адрес.

## Ограничения

- Лимит запросов: 10 запросов в минуту с одного IP
