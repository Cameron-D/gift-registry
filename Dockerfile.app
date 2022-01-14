FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE registry.settings.prod

WORKDIR /registry

RUN apk add --no-cache gcc musl-dev mariadb-connector-c-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "registry.wsgi:application"]