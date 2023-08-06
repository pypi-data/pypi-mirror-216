from django.contrib.postgres.operations import CreateExtension


class Q3CExtension(CreateExtension):
    def __init__(self):
        self.name = "q3c"
