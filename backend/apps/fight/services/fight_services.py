from ..models.fight import History, Fight


def desglozar(val):
    """
    Servicio para desglozar el json que entra entre personaje 1 y personaje 2
    :param val:
    :return: Character, Character
    """
    p1 = dict(val.get('character_p1'))
    p2 = dict(val.get('character_p2'))
    return p1, p2

def start_fight(pj1, pj2):
    """
    Servicio para determinar que personaje inicia primero en la batalla
    :return: String
    """
    try:
        movements_p1, hits_p1 = pj1.get('movements', None), pj1.get('hits', None)
        movements_p2, hits_p2 = pj2.get('movements', None), pj2.get('hits', None)
        totalp1, totalp2 = count_movs(movements_p1, hits_p1), count_movs(movements_p2, hits_p2)

        if totalp1 > totalp2 or count_hits(hits_p1) > count_hits(hits_p2):
            return 'P2'

    except Exception as e:
        print("Ocurrio un error en el servicio de start: ", str(e))

    return 'P1'

def count_movs(lista1, lista2):
    """
    Servicio que concatena los movimientos y ataques para luego contarlos
    :return: integer
    """
    count = 0
    try:
        for i, m in enumerate(lista1):
            count = len(m+lista2[i]) + count

        return count
    except Exception as e:
        print("Ocurrio un error en servicio de count_movs: ",str(e))


def count_hits(lista):
    """
    Servicio que solo cuennta los hits
    :param lista: Recibe lista con hits
    :return: integer
    """
    count = 0
    for h in lista:
        count = len(h)
    return count


def combination_movements(movements, hits):
    """
    Servicio que concatena los movimientos y los hits para devolver una lista de cada movimiento y hits
    por turno
    """

    movements_hits = []
    try:
        for i, m in enumerate(movements):
            movements_hits.append(m + hits[i])
    except Exception as e:
        print("Ocurrio un error en servicio 'combination_movements :  ",str(e))
    return movements_hits



def main_fight(start, pj1, pj2, fight):
    """
    La idea del servicio es realizar  lo necesario para registrar los ataques, descontar la engergia y
    definir el ganador, tiene dos formas dependiendo de quien comienza el ataque (Esto no lo alcance a optimizar pero claramente
    se puede)
    """
    vida_p1, vida_p2 = 6, 6
    try:
        atacks_p1 = combination_movements(pj1.get('movements', None), pj1.get('hits', None))
        atacks_p2 = combination_movements(pj2.get('movements', None), pj2.get('hits', None))
        win = False
        if start == 'P1':
            for x, y in zip(atacks_p1, atacks_p2):
                vida_p2, relato2 = attacks_energy(pj1, vida_p2, x, fight)
                vida_p1, relato1 = attacks_energy(pj2, vida_p1, y, fight)
                if vida_p2 <= 0:
                    win=True
                    ver_winner(pj1, fight, f"Gano {x.name} aun quedandole {vida_p1} de vida")
                    break
                elif vida_p1 <= 0:
                    win=True
                    ver_winner(pj2, fight, f"Gano {y.name} aun quedandole {vida_p2} de vida")
                    break
            if not win:
                ver_winner(pj1, fight, f"Empatee señoresss!")
        else:
            for x, y in zip(atacks_p1, atacks_p2):
                vida_p1, relato1 = attacks_energy(pj2, vida_p1, y, fight)
                vida_p2, relato2 = attacks_energy(pj1, vida_p2, x, fight)
                if vida_p2 <= 0:
                    win=True
                    ver_winner(pj1, fight, f"Gano {pj1.get('id', None).name} aun quedandole {vida_p1} de vida")
                    break
                elif vida_p1 <= 0:
                    win=True
                    ver_winner(pj2, fight, f"Gano {y.name} aun quedandole {vida_p2} de vida")
                    break
            if not win:
                ver_winner(pj1, fight, f"Empatee señoresss!")
        return True
    except Exception as e:
        print("Ocurrio un error en main_fight: ", str(e))
    return False

def attacks_energy(player, life, mov, fight):

    """
    Servicio complejo que determina el tipo de poder que se efectua en el turno,
    ademas de descontar la energia al contricante
    retornando la vida y relato del movimiento
    :return: integer, string
    """

    poderes =player.get('id').powers.all().exclude(combination__in=['P','K'])
    val = mov
    relato, relatv2 = "", ""
    try:
        for p in poderes:
            if mov.endswith(p.combination) :
                life = life - p.energy_attack
                val = mov.replace(p.combination, "")
                relatv2 = F'Utiliza el poder {p.name} sin piedad'
                break

        pl = 1 if Fight.character_p1 == player.get('id') else 2
        relato = relato_mov_service(relato, val, pl)

        if val.endswith(('P', 'K')):
            life = life - 1
            msg = " Pega un puño" if val.endswith('P') else "Pega una patada"
            relatv2 = relatv2 + msg

        relato = f'{player.get("id").name} {relato}  {relatv2}'
        History.objects.create(fight_mov=fight, movement=mov, turn="1", relato=relato,
                                              character=player.get('id'))
    except Exception as e:
        print("Ocurrio un error en 'attacks_energy' :", str(e))

    return life, relato



def ver_winner(player, fight, relato):

    """
    Servicio para verificar y guardar ganador en la base de datos.
    :return: True
    """
    try:
        History.objects.create(fight_mov=fight, movement='WIN', turn="10", relato=relato,
                               character=player.get('id',None))
        fight.winner = (player.get('id'))
        fight.save()
    except Exception as e:
        print("ocurrio un error en 'ver_winner' : ", str(e))
        return False

    return True


def relato_mov_service(relato, val, pj):

    """
    Servicio para determinar el relato de movimientos basicos y su lado segun el player seleccionado
    :return: string
    """
    try:
        for x in val:
            if x == "W":
                relato = f'{relato}  Salto '
            elif x == "A":
                relato = f'{relato} retrocede ' if pj == 1 else f'{relato} Avanzo'
            elif x == "S":
                relato = f'{relato} Se agacho '
            elif x == "D":
                relato = f'{relato}  Avanzo  ' if pj == 1 else f'{relato} Retrocede'
    except Exception as e:
        print("Ocurrio un error en 'relato_mov_service' : ",str(e))
    return relato

