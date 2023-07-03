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


class Task(AutoTimestamp):
    title = models.CharField("Title", max_length=200)
    description = models.TextField("Description", blank=True, null=True)
    expected_duration = models.DurationField("Expected Duration")
    final_duration = models.DurationField("Final Duration", blank=True, null=True)
    coin_reward = models.PositiveIntegerField("Coin Reward", default=0)
    fixed = models.BooleanField("Fixed", default=False)
    finished = models.BooleanField("Finished", default=False)
    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.CASCADE,
        default=User.objects.get(username="admin").id
    )

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Reward(AutoTimestamp):
    title = models.CharField("Title", max_length=200)
    description = models.TextField("Description", blank=True, null=True)
    duration = models.DurationField("Duration")
    cost = models.PositiveIntegerField("Cost", default=0)
    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.CASCADE,
        default=User.objects.get(username="admin").id
    )

    class Meta:
        verbose_name = "Reward"
        verbose_name_plural = "Rewards"
