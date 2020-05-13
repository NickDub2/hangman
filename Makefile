HANGMAN_RUN := docker-compose run --rm hangman
DJANGO_RUN := $(HANGMAN_RUN) python manage.py
POSTGRES_RUN := docker-compose run --rm db

image:
	@echo Rebuilding Hangman image...
	@docker-compose build --no-cache --force-rm hangman
	@docker-compose up -d

shell:
	@echo Starting bash inside container...
	@$(HANGMAN_RUN) bash

repl:
	@echo Starting Django shell...
	@$(DJANGO_RUN) shell_plus

check:
	@$(DJANGO_RUN) check

test:
	@$(HANGMAN_RUN) py.test api/tests --blockage

migrations:
	@$(DJANGO_RUN) makemigrations api

migrate:
	@$(DJANGO_RUN) migrate

