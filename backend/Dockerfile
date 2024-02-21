FROM python:3.11-alpine

WORKDIR /backend

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

RUN apk add --no-cache gcc musl-dev postgresql-dev libffi-dev

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install psycopg2-binary

COPY . .

RUN addgroup -S app-group && \
    adduser -S app-user -G app-group && \
    chown -R app-user:app-group /backend

USER app-user
