run:
	python manage.py runserver

setup:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

seed-database:
	python manage.py loaddata seed.json

test:
	python manage.py test
