



from rest_framework import serializers

from ..models.fight import Fight, History
from ..services.fight_services import desglozar, main_fight, start_fight
from ...character.models.character import Character

class CharacterPjsSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Character.objects.all())
    movements = serializers.ListField(child=serializers.CharField(max_length=5))
    hits = serializers.ListField(child=serializers.CharField(allow_null=True, allow_blank=True, max_length=1 ))

class FightSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    character_p1 = CharacterPjsSerializer()
    character_p2 = CharacterPjsSerializer()

    class Meta:
        model = Fight
        fields = '__all__'

    def create(self, validated_data):
        p1, p2 = desglozar(validated_data)
        instance = Fight.objects.create(character_p1=p1.get('id'), character_p2=p2.get('id'))
        main_fight(start_fight(p1, p2), p1,p2, instance)
        return instance

class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = ['relato']



