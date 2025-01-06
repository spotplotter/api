POETRY_RUN = poetry run
DOCKER_COMPOSE_OPTIONS = -f database/docker-compose.yml

# PostgreSQL
start-db:
	$(POETRY_RUN) docker-compose ${DOCKER_COMPOSE_OPTIONS} up --build -d

stop-db:
	$(POETRY_RUN) docker-compose ${DOCKER_COMPOSE_OPTIONS} down -v

connect-db:
	$(POETRY_RUN) docker exec -it spotplotter_postgres psql -U spotplotter -d spotplotter_db

# Python
install:
	poetry install

lint:
	$(POETRY_RUN) flake8 spotplotter/

format:
	$(POETRY_RUN) black spotplotter/

test:
	$(POETRY_RUN) pytest

run:
	SENDGRID_API_KEY="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" \
	EMAIL_FROM_ADDRESS="hello@spotplotter.com" \
	BASE_URL="http://127.0.0.1:3000" \
	DATABASE_URL="postgresql://spotplotter:spotplotterpassword@localhost/spotplotter_db" \
	JWT_SECRET="supersecretkey" \
	$(POETRY_RUN) uvicorn spotplotter.main:app --host 127.0.0.1 --port 8000 --reload

migrate:
	$(POETRY_RUN) alembic upgrade head

# Utilities
shell:
	$(POETRY_RUN) python

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache

help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:' Makefile | awk -F ':' '{print "  " $$1}'
