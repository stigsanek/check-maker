run:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

createsuperuser:
	poetry run python manage.py createsuperuser

install:
	poetry install

lint:
	poetry run flake8 check_maker

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=check_maker --cov-report xml
