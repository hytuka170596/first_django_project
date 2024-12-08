#!/bin/bash

set -e  # Остановить выполнение при ошибке

# Сбор статических файлов
echo "Сбор статических файлов..."
python manage.py collectstatic --noinput

# Проверка на наличие файла миграций
if [ ! -f /app/migrations_applied ]; then
    echo "Применение миграций..."
    python manage.py migrate
    touch /app/migrations_applied  # Создаем файл-флаг
else
    echo "Миграции уже были применены."
fi

exec "$@"  # Выполняем команду из CMD