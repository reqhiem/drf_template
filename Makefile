PYTHON := python #Change to python3 if you are using python3
MANAGE := ${PYTHON} manage.py
PORT := 8000

.PHONY: run
run:
	- ${MANAGE} runserver ${PORT}

.PHONY: makemigrations
makemigrations:
	- ${MANAGE} makemigrations

.PHONY: migrate
migrate:
	- ${MANAGE} migrate