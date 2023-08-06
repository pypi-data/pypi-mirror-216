# django-q3c

django-q3c is python package to add support for the q3c
(https://github.com/segasai/q3c) PostgreSQL extension to
the django ORM. This allows for spherical indexing for faster queries, and
avoids the need for manual SQL usage (thereby increasing security by avoiding
SQL injection attacks).

## Running the tests

In order to run the tests, you will need to have a PostgreSQL database with q3c
installed. To simplify things, a docker-compose file is provided to set one up.
The following is sufficient to run the tests:
```
sudo docker-compose
source db_source.sh
tox -r
```
