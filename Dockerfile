FROM python:3.7-slim
LABEL maintainer="fraph24@gmail.com"

WORKDIR /app
ADD poetry.lock pyproject.toml ./
RUN pip install poetry && \
    poetry install --no-root --no-dev
ADD . .

EXPOSE 8080
CMD ["/usr/local/bin/poetry", "run", "uvicorn", "api.index:app"]
