FROM python:3.13.3-slim
RUN curl -sSL https://install.python-poetry.org | python3 - \
 && ln -s /root/.local/bin/poetry /usr/local/bin/poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry instal --no-root --only main
COPY . .
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
