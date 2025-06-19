#!/bin/bash

# Установка необходимых компонентов
echo "Установка системных зависимостей..."
sudo apt-get update
sudo apt-get install -y \
    curl \
    python3 \
    python3-pip \
    python3-venv \
    docker.io \
    docker-compose

# Добавление текущего пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker

# Создание и активация виртуального окружения
echo "Создание виртуального окружения Python..."
python3 -m venv venv
source venv/bin/activate

# Установка Python-зависимостей
if [ -f "requirements.txt" ]; then
    echo "Установка зависимостей из requirements.txt..."
    pip3 install -r requirements.txt
else
    echo "Файл requirements.txt не найден, устанавливаю базовые зависимости..."
    pip3 install django djangorestframework psycopg2-binary
fi

# Сборка и запуск Docker-контейнеров
echo "Запуск Docker-контейнеров..."
docker-compose up -d --build
docker-compose build --no-cache
docker-compose up -d
docker-compose exec web python manage.py makemigrations animals
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py loaddata sections.json

echo "Готово! Проект должен быть доступен по адресу: http://localhost:8000"
