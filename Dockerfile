FROM python:3.11

WORKDIR /app

COPY . /app/core

EXPOSE 8000

RUN pip install poetry && poetry install --no-dev

CMD ["poetry", "run", "uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8000"]