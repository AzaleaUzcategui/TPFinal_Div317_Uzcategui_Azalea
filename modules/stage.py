import json
import random
from pathlib import Path

# Config mínima de respaldo: solo la ruta del setup.
DEFAULT_CONFIG: dict = {
    "setup_path": "modules/stage_setup.json"
}


def cargar_config(config_path=None) -> dict:
    path = Path(config_path or DEFAULT_CONFIG.get("setup_path"))
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def sumar_stats(deck: list) -> dict:
    return {
        "hp": int(sum(card.get("hp", 0) for card in deck)),
        "atk": int(sum(card.get("atk", 0) for card in deck)),
        "def": int(sum(card.get("def", 0) for card in deck)),
    }


def armar_player(name: str, deck: list) -> dict:
    base_stats = sumar_stats(deck)
    return {
        "name": name,
        "deck": [card.copy() for card in deck],
        "discard": [],
        "stats": base_stats.copy(),
        "base_stats": base_stats,
        "score": 0,
        "heal_available": True,
        "shield_available": True,
        "shield_on": False,
        "last_card": None
    }


def parsear_nombre_carta(file_path: Path) -> dict:
    """
    Extrae datos del nombre de archivo y los pone en una lista (separando por
    '_'), luego los asigna a su respectiva variable y pum, diccionario!!!!
    """
    name_no_ext = file_path.stem #nombre sin extension
    partes = name_no_ext.split("_")

    hp = int(partes[2]) if len(partes) > 2 and partes[2].isdigit() else 0
    atk = int(partes[4]) if len(partes) > 4 and partes[4].isdigit() else 0
    defense = int(partes[6]) if len(partes) > 6 and partes[6].isdigit() else 0
    stars = int(partes[7]) if len(partes) > 7 and partes[7].isdigit() else 1

    return {
        "name": name_no_ext,
        "hp": hp,
        "atk": atk,
        "def": defense,
        "stars": stars,
        "image_path": str(file_path),
        "deck": file_path.parent.name
    }


def cargar_cartas_carpeta(folder: Path) -> list:
    """
    De vuelve una lista con las cartas de la carpeta, saltando las que tengan
    reverse (esas no las queremos mostrar aca)
    """
    cards = []
    for file in folder.glob("*.png"): #Iterador de rutas 
        if "reverse" in file.stem.lower():
            continue
        cards.append(parsear_nombre_carta(file))
    return cards


def elegir_cartas_random(folder: Path, cantidad: int) -> list:
    """
    Toma la carpeta y la cantidad, y devuelve una lista de cartas randomizadas
    """
    cartas = cargar_cartas_carpeta(folder)
    if cantidad > len(cartas):
        cantidad = len(cartas)
    return random.sample(cartas, cantidad)


def construir_mazo(deck_root: Path, cantidades: dict) -> list:
    """
    Crea el mazo vacío, concatena las cartas por carpeta y después las mezcla
    para que no queden una detrás de la otra
    """
    mazo = []
    for nombre_carpeta, cantidad in cantidades.items():
        carpeta = deck_root / nombre_carpeta
        if carpeta.exists() and carpeta.is_dir():
            mazo.extend(elegir_cartas_random(carpeta, cantidad))
    random.shuffle(mazo) #shuflea JAJAJA
    return mazo



def iniciar_stage(config_path=None, preset_config=None) -> dict:
    """
    Carga config, busca nivel (cantidad de cartas x carpeta) y deck_root.
    Arma los dos mazos con los requisitos por config.
    Mezcla los mazos y retorna el estado del stage (inicial por ahora)
    
    """
    config = preset_config if preset_config is not None else cargar_config(config_path)
    nivel = config.get("nivel", "nivel_1") #Nivel -> cantidades de carytas basically
    deck_root = Path(config.get("deck_root", "assets/img/decks"))

    requisitos = config.get("deck_requirements") or config.get(nivel, {}).get("cantidades", {})

    player_deck = construir_mazo(deck_root, requisitos)
    enemy_deck = construir_mazo(deck_root, requisitos)

    player = armar_player("Jugador", player_deck)
    enemy = armar_player("CPU", enemy_deck)
    mezclar_mazos(player, enemy)

    return {
        "config": config,
        "player": player,
        "enemy": enemy,
        "time_left_ms": int(config.get("stage_time_ms", 120_000)),
        "finished": False,
        "finished_reason": "",
        "score_sent": False
    }


def reiniciar_stage(stage: dict) -> None:
    """
    Setea todo a como estaba inicialmente y actualiza el diccionario
    """
    config = stage.get("config", DEFAULT_CONFIG)
    new_stage = iniciar_stage(None, preset_config=config)
    stage.clear()
    stage.update(new_stage)


def mezclar_mazos(player: dict, enemy: dict) -> None:
    """
    Shuflea los mazos
    """
    random.shuffle(player["deck"])
    random.shuffle(enemy["deck"])


def robar_cartas(player: dict, enemy: dict):
    """
    Si no hay mazos, no devuelve nada.
    En caso de haber, saca la ultima carta de cada uno.
    las deja en "last_card" y de paso, las deja en discard,
    para no volver a llamarlas.
    """
    if not player["deck"] or not enemy["deck"]:
        return None, None
    carta_jugador = player["deck"].pop(0)
    carta_enemy = enemy["deck"].pop(0)
    player["last_card"] = carta_jugador
    enemy["last_card"] = carta_enemy
    player["discard"].append(carta_jugador)
    enemy["discard"].append(carta_enemy)
    return carta_jugador, carta_enemy


def ataque_carta_con_bonus(card: dict, bonus_map: dict) -> float:
    """
    Dependiendo de la estrella - > bonus
    Obtiene las estrellas, busca el bonus en bonus_map, un diccionario con los valores, y
    devuelve el valor del ataque con el bonus
    """
    stars = int(card.get("stars", 1))
    bonus_pct = card.get("bonus", bonus_map.get(str(stars), 0))
    return card.get("atk", 0) * (1 + bonus_pct)


def stats_carta_con_bonus(card: dict, bonus_map: dict, crit_multiplier: int) -> dict:
    """
    Dependiendo del bonus, devuelve diccionario con hp,atk y def con el bonus (y el critico)
    aplicados
    """
    stars = int(card.get("stars", 1))
    bonus_pct = card.get("bonus", bonus_map.get(str(stars), 0))
    return {
        "hp": int(card.get("hp", 0) * (1 + bonus_pct) * crit_multiplier),
        "atk": int(card.get("atk", 0) * (1 + bonus_pct) * crit_multiplier),
        "def": int(card.get("def", 0) * (1 + bonus_pct) * crit_multiplier)
    }


def elegir_critico(criticos: list) -> int:
    """
    El gambling de los criticos jije (con lista x las dudas)
    """
    return random.choice(criticos or [1, 1, 2])


def aplicar_daño(target: dict, damage: dict) -> None:
    """
    resta los stats del target, sin bajar de 0.
    le dejo valor por defecto 0 para que no rompa todo
    """
    for stat in ("hp", "atk", "def"):
        target["stats"][stat] = max(0, int(target["stats"].get(stat, 0) - damage.get(stat, 0)))


def aplicar_heal(player: dict) -> None:
    """
    OP HEAL
    Sana al player a su vida original (OP!!!)
    """
    player["stats"] = player.get("base_stats", {}).copy()
    player["heal_available"] = False #De paso lo flageo para que no lo vuelva  usar


def activar_shield(player: dict) -> None:
    """
    Activa escudo
    """
    player["shield_on"] = True
    player["shield_available"] = False


def resolver_mano(player: dict, enemy: dict, config: dict) -> dict:
    """
    Funcion que lo une todo:
     'roba' cartas del mazo
     calcula los bonus y los criticos
     calcula los puntajes y al ganador
     aplica el daño -> Hasta considera el escudo como espero, para que devuelva
     
    Devuelve un diccionario con la informacion del ganador.
    
    """
    bonus_map = config.get("bonus_by_stars", {})
    crit_pool = config.get("critical_pool", [1, 1, 2])
    points_per_hand = int(config.get("points_per_hand", 100))

    player_card, enemy_card = robar_cartas(player, enemy)
    if not player_card or not enemy_card:
        return {"finished": True, "reason": "deck_empty"} #Si se acaban las cartas, termina


    #Bonuses
    player_attack = ataque_carta_con_bonus(player_card, bonus_map)
    enemy_attack = ataque_carta_con_bonus(enemy_card, bonus_map)
    crit = elegir_critico(crit_pool)

    #ganadores
    player_wins = player_attack >= enemy_attack
    winner = player if player_wins else enemy
    loser = enemy if player_wins else player
    winner_card = player_card if player_wins else enemy_card


    mirror_damage = loser.get("shield_on", False)
    if mirror_damage:
        loser["shield_on"] = False

    damage_target = loser if not mirror_damage else winner
    damage_stats = stats_carta_con_bonus(winner_card, bonus_map, crit)
    aplicar_daño(damage_target, damage_stats)

    score_gain = points_per_hand
    if player_wins:
        player["score"] += score_gain
    else:
        enemy["score"] += score_gain

    return {
        "finished": False,
        "crit": crit,
        "player_wins": player_wins,
        "mirror": mirror_damage,
        "p_card": player_card,
        "e_card": enemy_card,
        "damage": damage_stats,
        "score_gain": score_gain
    }


def chequear_fin_partida(player: dict, enemy: dict, time_left_ms: int) -> tuple:
    """
    RAZONES DE FINISH
    """
    if player["stats"]["hp"] <= 0:
        return True, "player_hp_zero"
    if enemy["stats"]["hp"] <= 0:
        return True, "enemy_hp_zero"
    if time_left_ms <= 0:
        return True, "time_over"
    if not player["deck"] or not enemy["deck"]:
        return True, "deck_empty"
    return False, ""


def tic_del_stage(stage: dict, delta_ms: int) -> tuple:
    """
    Timer del stage. Chequea si terminó la partida y devuelve la razon.
    """
    stage["time_left_ms"] = max(0, int(stage.get("time_left_ms", 0) - delta_ms))
    finished, reason = chequear_fin_partida(stage["player"], stage["enemy"], stage["time_left_ms"])
    if finished:
        stage["finished"] = True
        stage["finished_reason"] = reason
    return finished, reason
