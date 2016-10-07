from __future__ import unicode_literals

from django.db import models


class Account(models.Model):
    _id = models.CharField(max_length=255)
    transfer_threshold = models.FloatField(default=2)
    pend_transfer = models.FloatField(default=0)


class Transaction(models.Model):
    account = models.ForeignKey('Account')
    _id = models.CharField(max_length=255)
    amount = models.FloatField()
