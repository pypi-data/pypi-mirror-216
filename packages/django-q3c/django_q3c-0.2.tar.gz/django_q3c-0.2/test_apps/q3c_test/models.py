from django.db import models

from django_q3c.indexes import Q3CIndex


class Position(models.Model):
    ra = models.FloatField()
    dec = models.FloatField()

    class Meta:
        indexes = [Q3CIndex(ra_col="ra", dec_col="dec")]

