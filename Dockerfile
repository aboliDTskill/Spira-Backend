FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove --purge -y build-essential python3-dev gcc \
    && apt-get autoremove -y \
    && apt-get clean

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Spira.wsgi:application"]
