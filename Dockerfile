FROM python:3.12.2-slim

# Container env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Container Working Directory
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]