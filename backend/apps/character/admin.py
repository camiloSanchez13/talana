from django.contrib import admin
# Register your models here.
from ..character.models.character import Character
from ..character.models.powers import Power

admin.site.register(Character)
admin.site.register(Power)