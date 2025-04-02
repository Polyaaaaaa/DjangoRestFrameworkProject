FROM python:3.9

# Устанавливаем рабочую директорию в контейнере
WORKDIR /code

# Устанавливаем зависимости
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /code/

# Открываем порт для сервера
EXPOSE 8000

# Команда по умолчанию для контейнера
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
