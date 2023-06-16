from django.contrib.auth.models import AbstractUser
from django.db import models


class AutoTimestamp(models.Model):
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, AutoTimestamp):
    coins = models.IntegerField("Coins", default=0)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
