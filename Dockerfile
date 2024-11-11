# Використовуємо базовий образ Python
FROM python:3.9-slim

# Встановлюємо робочу директорію для додатку
WORKDIR /app

# Копіюємо файл вимог
COPY requirements.txt .

# Встановлюємо всі залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проекту в контейнер
COPY . .

# Налаштовуємо змінну середовища для Django
ENV PYTHONUNBUFFERED 1

# Відкриваємо порт, який використовує Django (за замовчуванням порт 8000)
EXPOSE 8000

# Запускаємо сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
