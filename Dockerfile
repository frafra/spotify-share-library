FROM python:3.7-slim

WORKDIR /app
ADD poetry.lock pyproject.toml ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install
ADD . .

EXPOSE 8080
CMD ["/usr/local/bin/python", "/app/spotify-share-library.py"]

