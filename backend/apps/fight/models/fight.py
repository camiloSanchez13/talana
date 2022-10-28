
from django.db import models

from ...character.models.character import Character


class Fight(models.Model):

    date_start = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField(auto_now=True, blank=True, null=True)

    character_p1 = models.ForeignKey(Character, on_delete=models.CASCADE,
                                     related_name="characterp1") #Personaje player 1
    character_p2 = models.ForeignKey(Character, on_delete=models.CASCADE,
                                     related_name="characterp2")  # Personaje player 2

    winner = models.ForeignKey(Character, on_delete=models.CASCADE,
                                     related_name="winnerpl", null=True, blank=True)


    def __str__(self):
        return f'{self.character_p1} VS {self.character_p2}'


class History(models.Model):
    fight_mov = models.ForeignKey(Fight, on_delete=models.CASCADE, related_name='history')
    character = models.ForeignKey(Character, on_delete=models.CASCADE,
                                     related_name="historial")
    movement = models.CharField(max_length=4, null=True, blank=True)
    turn = models.PositiveIntegerField()
    relato = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.movement