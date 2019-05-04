# reviews
Django application for submitting company reviews

## Prerequisites

* python 3.6

* .env ini file with DJANGO_ENV value and passwords at the same level as manage.py. 
See settings.py and config directory for example settings.

* pipenv

## Install requirements using pipenv
* PIPENV_VENV_IN_PROJECT=1 pipenv --python 3.6
* pipenv sync or pipenv sync --dev for development tools
* pipenv shell

## Run test suite with coverage
* coverage run manage.py test

## Run django migrations
* python manage.py migrate

## Run application
* python manage.py runserver