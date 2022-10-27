from rest_framework import serializers

from .power_serializer import PowerSerializer
from ..models.powers import Power
from ...character.models.character import Character


class CharacterSerializer(serializers.ModelSerializer):

    powers = serializers.SerializerMethodField()

    @staticmethod
    def get_powers(obj: Character):
        return PowerSerializer(obj.powers.all(), many=True).data

    class Meta:
        model = Character
        fields = '__all__'



class CharacterDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model=Power
        fields = '__all__'
        depth = 2