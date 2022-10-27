
from rest_framework import viewsets

from pagination import TwentyResultsPagination
from ..serializers.character_serialzier import CharacterSerializer
from ..serializers.power_serializer import PowerSerializer
from ...character.models.character import Character
from ...character.models.powers import Power

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    pagination_class = TwentyResultsPagination





class PowerViewSet(viewsets.ModelViewSet):
    queryset = Power.objects.all()
    serializer_class = PowerSerializer
    pagination_class = TwentyResultsPagination
