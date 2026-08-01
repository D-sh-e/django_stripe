# Dockerfile
FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 \ 
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Открытие порта
EXPOSE 8000


# Запуск приложения
CMD sh -c "python manage.py migrate --noinput && \
           python manage.py collectstatic --noinput && \
           python manage.py loaddata data.json --noinput && \
           gunicorn --bind 0.0.0.0:8000 stripe_project.wsgi:application"


