from django.db.models import Index

from .expressions import Q3CAng2IPix


class Q3CIndex(Index):
    # Postgres has a maximum length of 63 (64 - 1), as we're only postgres,
    # allow a longer length.
    max_name_length = 63

    # PostgresIndex would be nice to use, but it's explicitly written to change
    # which mechanism is used to store the index

    def __init__(self, *, ra_col, dec_col, name=None, name_hint=None):
        # TODO: check whether any of the additional options that can be set on
        # indexes will work with q3c, a quick look implies not
        self.ra_col = ra_col
        self.dec_col = dec_col
        index_expression = Q3CAng2IPix(ra_col=ra_col, dec_col=dec_col)
        if name is None:
            name = self._generate_example_name(name_hint)
        super().__init__(index_expression, name=name)

    def _generate_example_name(self, name_hint=None):
        if name_hint is None:
            name_hint = ""
        return "_".join(["q3c", self.ra_col, self.dec_col, name_hint])

    def deconstruct(self):
        path, args, kwargs = super().deconstruct()
        kwargs["ra_col"] = self.ra_col
        kwargs["dec_col"] = self.dec_col
        # We accept no args, drop them
        return path, [], kwargs
