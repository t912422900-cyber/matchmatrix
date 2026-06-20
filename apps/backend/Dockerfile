FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY apps/backend/pyproject.toml ./pyproject.toml
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

COPY apps/backend/app ./app
COPY apps/backend/alembic ./alembic
COPY apps/backend/alembic.ini ./alembic.ini

EXPOSE 8000

CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
