# reviews
Django application for submitting company reviews via an API.

Supports the following:

1. Users can register for the system via the API.
2. Users can get an authentication token via the API.
2. Authenticated users can create and edit their own reviews.
3. Authenticated users can read their own reviews.
4. Django Admin users can manage all Companies, Reviews, and Reviewers via Django Admin


## Prerequisites

* python 3.6

* pipenv

* Needs a .env ini file with DJANGO_ENV value and passwords at the same level as manage.py. 
See .env_sample, config directory, and settings.py for example settings.

## Install requirements using pipenv
* PIPENV_VENV_IN_PROJECT=1 pipenv --python 3.6
* pipenv sync or pipenv sync --dev for development tools
* pipenv shell

## Run test suite with coverage
* coverage run manage.py test
* coverage html

## Run django migrations
* python manage.py migrate

## Create a django admin user
* python manage.py createsuperuser

## Add sample companies, reviewers, and reviews 
* fixtures.json has sample companies, reviewers, and reviews
* fixture user passwords are all F9aSEvbSfkeYByKG

## Run application
* python manage.py runserver