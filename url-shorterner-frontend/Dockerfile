# Этап сборки
FROM node:20-slim as build

WORKDIR /app

# Копируем только файлы зависимостей сначала для лучшего кэширования
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Затем копируем остальные файлы
COPY . .

# Собираем приложение
RUN yarn build

# Этап production
FROM nginx:stable-alpine

# Копируем собранные файлы из этапа сборки
COPY --from=build /app/dist /usr/share/nginx/html

# Копируем конфигурацию nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 