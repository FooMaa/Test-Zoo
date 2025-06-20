# Test-Zoo
### Как запускаемся (Linux/Unix)?

```bash
# Установка необходимых компонентов
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
python3 -m venv venv
source venv/bin/activate

# Установка Python-зависимостей
pip3 install -r requirements.txt

# Сборка и запуск Docker-контейнеров
sudo docker-compose build --no-cache
sudo docker-compose up -d
sudo docker-compose exec web python manage.py makemigrations animals
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py loaddata sections.json
sudo docker-compose exec web python manage.py createsuperuser

#Готово! Проект должен быть доступен по адресу: http://localhost:8000"
```

### Описание API

Для опробации API ставим:
```bash
sudo apt install httpie
```
Запросы:
```bash
# Вывести всех животных
http GET http://127.0.0.1:8000/api/animals/

# Вывести одно животное
http GET http://127.0.0.1:8000/api/animals/1/

# Создать животное
http POST http://127.0.0.1:8000/api/animals/ \
    name="Барсик" \
    species="Кошка" \
    birth_date="2020-01-01" \
    section_id=1

# Обновить животное
http PUT http://127.0.0.1:8000/api/animals/1/ \
    name="Барсик (Обновленный)" \
    species="Кошка" \
    birth_date="2020-01-01" \
    section_id=1

# Добавить процедуру
http POST http://127.0.0.1:8000/api/animals/2/procedures/ \
   procedure_type="WEIGHT" \
   details="Годовая прививка"

# Получить процедуры у животного
http GET http://127.0.0.1:8000/api/animals/2/procedures/

# Частично обновить животное
http PATCH http://127.0.0.1:8000/api/animals/1/ \
    name="Новое имя"

# Удалить животное
http DELETE http://127.0.0.1:8000/api/animals/1/
```
