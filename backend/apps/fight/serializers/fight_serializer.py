



from rest_framework import serializers

from ..models.fight import Fight, History
from ...character.models.character import Character


#TODO MOSTRAR MENSAJE DE ERRORES EN SERIALIZER EJ raise serializers.ValidationError({'driver': ['This driver is assigned to another bus.']})
from ...character.models.powers import Power


class CharacterPjsSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Character.objects.all())
    movements = serializers.ListField(child=serializers.CharField())
    hits = serializers.ListField(child=serializers.CharField(allow_null=True, allow_blank=True))

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

        # obtenerMovimientos(p1, p2)
        main_fight(startFight(p1, p2), p1,p2, instance)
        # History.objects.bulk_create([History(fight_mov=instance, movement=p1.get('movements', None), turn="1", hit="Patada", character=p1.get('id')),
        #                              History(fight_mov=instance, movement=p2.get('movements', None), turn="1", hit="Combo",
        #                                      character=p2.get('id'))])
        return instance

    # def update(self, instance: Fight, validated_data):
    #     p1, p2 = desglozar(validated_data)
    #     History.objects.bulk_create([History(fight_mov=instance, movement=p1.get('movement', None), turn="1", hit="Patada",
    #                                          character=p1.get('id')),
    #                                  History(fight_mov=instance, movement=p2.get('movement', None), turn="1", hit="Combo",
    #                                          character=p2.get('id')),
    #                                  ])
    #
    #     obtenerMovimientos(p1, p2)
    #     return True


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = ['relato']
#TODO: MOVER A SERVICIOS y CREAR SERVICIOS PARA CREAR HISTORIAL DE MOVIMIENTOS

def desglozar(val):
    p1 = dict(val.get('character_p1'))
    p2 = dict(val.get('character_p2'))
    return p1, p2

def obtenerMovimientos(value1, value2):

    movements = value1.get('movements', None)
    hits = value1.get('hits', None)
    characters = "PK"
    print('movimientos_especiales: ',hits)
    print('movimientos_normales', movements)
    startFight(movements,hits )
    return None

def obtenerPoderes(pj, valor):
    if Power.objects.filter(combination=valor, character=pj).exists():

        return Power.objects.get(combination=valor, character=pj).name

    return None

def startFight(pj1, pj2):

    movements_p1, hits_p1 = pj1.get('movements', None), pj1.get('hits', None)
    movements_p2, hits_p2 = pj2.get('movements', None), pj2.get('hits', None)
    totalp1, totalp2 = countMovs(movements_p1, hits_p1), countMovs(movements_p2, hits_p2)

    if totalp1 > totalp2 or countHits(hits_p1) > countHits(hits_p2):
        return 'P2'

    return 'P1'

def countMovs(lista1, lista2):

    count = 0
    for i, m in enumerate(lista1):
        count = len(m+lista2[i]) + count

    return count


def countHits(lista):
    count = 0
    for h in lista:
        count = len(h)
    return count


def combination_movements(movements, hits):

    movements_hits = []
    for i, m in enumerate(movements):
        movements_hits.append(m + hits[i])

    print("los movimientos mas hits son : ", movements_hits )
    return movements_hits



def main_fight(start, pj1, pj2, fight):
    relato2 = ""
    relato1 = ""
    #TODO OPTIMIZAR EL POR EL CUAL COMIENZA
    vida_p1, vida_p2 = 6, 6
    atacks_p1 = combination_movements(pj1.get('movements', None), pj1.get('hits', None))
    atacks_p2 = combination_movements(pj2.get('movements', None), pj2.get('hits', None))

    if start == 'P1':
        for x, y in zip(atacks_p1, atacks_p2):
            relato2=""
            relato1=""
            vida_p2, relato2 = attacks_energy(pj1, vida_p2, x, fight)
            # print(f"se comenzo por el player 2 y mando estos datos : vida : {vida_p2} y relato {relato1} y movimiento {x}")
            vida_p1, relato1 = attacks_energy(pj2, vida_p1, y, fight)
            if vida_p2 <= 0:
                print("relato1 ", relato1)
                print("relato2 ", relato2)
                print("gano el p1")
                break
            elif vida_p1 <= 0:
                print("relato1 ", relato1)
                print("relato2 ", relato2)
                print("gano el p2")
                break
    else:
        for x, y in zip(atacks_p1, atacks_p2):
            relato2 = ""
            relato1 = ""
            vida_p1, relato1 = attacks_energy(pj2, vida_p1, y, fight)
            vida_p2, relato2 = attacks_energy(pj1, vida_p2, x, fight)
            # print("vida del p2 ;", vida_p2)
            # print("vida del p1 ;", vida_p1)
            if vida_p2 <= 0:
                print("Gano el p1")
                break
            elif vida_p1 <= 0:
                print("Gano el P2")
                break

def attacks_energy(player, life, mov, fight):


    #TODO falta separar de los movimientos los poderes :
    poderes =player.get('id').powers.all().exclude(combination__in=['P','K'])
    val = mov
    relato = ""
    relatv2=""
    print(f"movimiento a relatar {val} del player llamado : {player.get('id')}")
    # print(f"movimiento a revisar : {val} del player {player.get('id')}")
    for p in poderes:
        if mov.endswith(p.combination) :
            life = life - p.energy_attack
            val = mov.replace(p.combination, "")
            relatv2 = F'Utiliza el poder {p.name} sin piedad'
            break
    if val.endswith(('P', 'K')):
        life = life - 1
        print("si termina en P o K el valor ", val)
        relatv2 = relatv2 + "Pega una patada o puño"
    # if Power.objects.filter(character=player.get('id'), combination=mov).exists():
    #     life = life - Power.objects.get(character=player.get('id'), combination=mov).energy_attack
    else:
        for x in val:
            if x == "W":
                relato = f'{relato}  Salto '
            elif x == "A":
                relato = f'{relato} retrocede '  #si es  player uno o dos ver para donde camina
            elif x == "S":
                relato = f'{relato} Se agacho '
            elif x == "D":
                relato = f'{relato}  Avanzo  '

    relato = f'{player.get("id").name} {relato}  {relatv2}'
    History.objects.create(fight_mov=fight, movement=mov, turn="1", relato=relato,
                                              character=player.get('id'))
    print("el relato es : ", relato)
    return life, relato
