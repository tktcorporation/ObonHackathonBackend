FROM python:3.9.6-slim-buster

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
ENV PYTHONPATH=/app
ENV MYPYPATH=out
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN apt update
RUN apt install -y git

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app

# コンテナ内で仮想環境の作成を無効
RUN poetry config virtualenvs.create false
RUN poetry config virtualenvs.in-project true

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry install

COPY . .

RUN poetry install

EXPOSE 8000

CMD [ "/bin/bash", "-c", "poetry run /app/manage.py runserver 0.0.0.0:8000" ]