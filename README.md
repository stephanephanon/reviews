# reviews
Django application for submitting company reviews via an API.

Supports the following:

1. Users can register for the system via the API
2. Users can get an authentication token via the API.
2. Authenticated users can write reviews
3. Authenticated users can read their own reviews.
4. Django Admin users can manage all Companies, Reviews, and Reviewers


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