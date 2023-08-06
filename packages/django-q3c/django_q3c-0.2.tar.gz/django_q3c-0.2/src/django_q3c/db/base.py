from django.db.backends.postgresql.base import (
    DatabaseWrapper as Psycopg2DatabaseWrapper,
)


class Q3CDatabaseWrapperMixin:
    def prepare_database(self):
        super().prepare_database()
        # Ensure that q3c is installed and set up.
        # This assumes that we do not need to update q3c, this is the same as
        # what geodjango does with postgis
        with self.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS q3c")


class DatabaseWrapper(Q3CDatabaseWrapperMixin, Psycopg2DatabaseWrapper):
    # databases need to be stored in base.py with the name DatabaseWrapper
    pass
