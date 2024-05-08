SHELL := /bin/bash

all: test

init:
	poetry config virtualenvs.create false --local
	poetry update

test:
	pytest -v --cov ./unchained --cov-report term-missing
