



from rest_framework import serializers

from ..models.fight import Fight
from ...character.models.character import Character


class FightSerializer(serializers.ModelSerializer):

    character_p1 = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all())
    character_p2 = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all())
    movement = serializers.CharField()


    class Meta:
        model = Fight
        fields = '__all__'