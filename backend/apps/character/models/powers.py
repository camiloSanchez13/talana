from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from ...character.models.character import Character


class Power(models.Model):

    name = models.CharField(max_length=40, null=False, blank=False)
    combination = models.CharField(max_length=5, null=False, blank=False)
    energy_attack = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='powers')

    class Meta:
        ordering = ['energy_attack']


    def __str__(self):
        return self.name