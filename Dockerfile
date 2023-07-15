FROM python:3.11-slim-buster

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry==1.5.1
RUN poetry install --no-root --no-dev
COPY . /app

EXPOSE 8000
CMD ["poetry", "run", "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
