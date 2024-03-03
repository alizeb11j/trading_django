from django.db import models

from django.utils import timezone


class Kraken(models.Model):
    BTC = models.FloatField()
    Price = models.FloatField()
    kra_time_update = models.DateTimeField(default=timezone.now)


class AltCoin(models.Model):

    Price = models.FloatField()
    alt_time_update = models.DateTimeField(default=timezone.now)
