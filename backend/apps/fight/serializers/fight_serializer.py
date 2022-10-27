



from rest_framework import serializers

from ..models.fight import Fight, History
from ...character.models.character import Character


#TODO MOSTRAR MENSAJE DE ERRORES EN SERIALIZER EJ raise serializers.ValidationError({'driver': ['This driver is assigned to another bus.']})
from ...character.models.powers import Power


class CharacterPjsSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Character.objects.all())
    movement = serializers.CharField(required=False)


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
        History.objects.bulk_create([History(fight_mov=instance, movement=p1.get('movement', None), turn="1", hit="Patada", character=p1.get('id')),
                                     History(fight_mov=instance, movement=p2.get('movement', None), turn="1", hit="Combo",
                                             character=p2.get('id'))])
        return instance

    def update(self, instance: Fight, validated_data):
        p1, p2 = desglozar(validated_data)
        History.objects.bulk_create([History(fight_mov=instance, movement=p1.get('movement', None), turn="1", hit="Patada",
                                             character=p1.get('id')),
                                     History(fight_mov=instance, movement=p2.get('movement', None), turn="1", hit="Combo",
                                             character=p2.get('id')),
                                     ])

        obtenerMovimientos(p1, p2)
        return True



#TODO: MOVER A SERVICIOS y CREAR SERVICIOS PARA CREAR HISTORIAL DE MOVIMIENTOS

def desglozar(val):
    p1 = dict(val.get('character_p1'))
    p2 = dict(val.get('character_p2'))

    return p1, p2


#TODO: FALTA SEPARAR LOS MOVIMIENTOS ESPECIALES DE LOS MOVIMIENTOS NORMALS ES DECIR PUEDE SER AA Y LUEGO EL PODER DSDP ENTONCES HAYQ
#MODIFICAR LA QUERY Y ADEMAS DE AGREGAR LOS PODERES Y MOVIMIENTOS POR LOS DOS PJ,

def obtenerMovimientos(value1, value2):

    teclas = value1.get('movement', None)
    characters = "PK"
    movimientos_especiales = obtenerPoderes(value1.get('id', None), teclas.upper())
    movimientos_normales = ''.join( x for x in teclas.upper() if x not in characters)
    print('movimientos_especiales: ',movimientos_especiales)
    print('movimientos_normales', movimientos_normales)
    return None

def obtenerPoderes(pj, valor):
    if Power.objects.filter(combination=valor, character=pj).exists():

        return Power.objects.get(combination=valor, character=pj).name

    return None