FROM python:3.12.3-bullseye


COPY . /unchained
WORKDIR /unchained

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install