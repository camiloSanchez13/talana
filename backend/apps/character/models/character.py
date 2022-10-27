from django.db import models
from django.utils import timezone


class Character(models.Model):
    name = models.CharField(max_length=30)
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
