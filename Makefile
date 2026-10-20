PYTHON ?= python

.PHONY: install run migrate revision test lint format hooks

install:
	$(PYTHON) -m pip install -e "backend[dev]"

hooks:
	$(PYTHON) -m pre_commit install

run:
	cd backend && $(PYTHON) -m uvicorn app.main:app --reload

migrate:
	cd backend && $(PYTHON) -m alembic upgrade head

revision:
	cd backend && $(PYTHON) -m alembic revision --autogenerate -m "$(m)"

test:
	cd backend && $(PYTHON) -m pytest

lint:
	cd backend && $(PYTHON) -m ruff check .
	cd backend && $(PYTHON) -m ruff format --check .
	cd backend && $(PYTHON) -m mypy

format:
	cd backend && $(PYTHON) -m ruff format .
	cd backend && $(PYTHON) -m ruff check --fix .
