FROM python:3.10.2-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/prod.txt ./requirements/prod.txt
RUN pip install --upgrade pip \
 && pip wheel --wheel-dir=/wheels -r requirements/prod.txt

# RUN pip wheel --wheel-dir=/wheels gunicorn>=21.2

FROM python:3.10.2-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

COPY . .

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=config.settings.prod

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
