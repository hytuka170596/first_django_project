#!/bin/bash

set -e  # Остановить выполнение при ошибке

echo "Сбор статических файлов..."
python manage.py collectstatic --noinput

echo "Применение миграций..."
python manage.py migrate
