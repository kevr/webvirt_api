webvirt_api
-----------

![lint](https://github.com/kevr/webvirt_api/actions/workflows/lint.yaml/badge.svg?branch=master)
![tests](https://github.com/kevr/webvirt_api/actions/workflows/tests.yaml/badge.svg?branch=master)

Back-end API for the webvirt application (driven by [Django](https://www.djangoproject.com/)).

Installation
------------

webvirt uses the [Poetry](https://python-poetry.org/) Python package manager
to deal with project information, dependencies and installation.

- The `--no-root` option excludes the project installation from installation
- The `--only-main` option excludes development dependencies from installation

#### Install dependencies

    $ poetry install [--only-main] --no-root

#### Install the project

    $ poetry install [--only-main]

Testing
-------

Running project tests expects that you've installed all depenencies,
including development dependencies, via [Poetry](https://python-poetry.org/):

    $ poetry install --no-root

To run all unit tests:

    ## With Poetry
    $ poetry run python manage.py test

    ## Without Poetry
    $ python manage.py test

Preparing the database
----------------------

When utilizing webvirt_api's default database,
[SQLite](https://www.sqlite.org/index.html), users can immediately migrate
to configure the schema:

    $ python manage.py migrate

Running the API
---------------

#### Development server

After [installation](#installation) and
[preparing the database](#preparing-the-database), users can run Django's
development server:

    $ python manage.py runserver

#### Serving in production

Users wishing to serve this API in production should get familiar with
[Django's uWSGI documentation](https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/uwsgi/),
as the project will need to be served using a WSGI backend like `uwsgi` as a
backend to web server software like [nginx](https://www.nginx.com/) or
[apache](https://www.apache.org/).

The following environment variables should be set when running in
production:

- `DEBUG=0`
- `SECRET_KEY='your_production_secret_key'`

Interested In Contributing?
---------------------------

Contributions of all kinds are welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md) for a detailed run-down of
contribution and style expectations.

Licensing
---------

This project operates under the [Apache 2.0 LICENSE](LICENSE) along with
an [Apache 2.0 NOTICE](NOTICE) which contains attributions of work.
