import json
import random
from pathlib import Path
from typing import Dict, List, Tuple

Card = Dict[str, float]
Deck = List[Card]
PlayerState = Dict[str, object]

# Default configuration used when no JSON is provided.
DEFAULT_CONFIG: Dict[str, object] = {
    "stage_time_ms": 120_000,
    "points_per_hand": 150,
    "points_mode": "fixed",  # fixed | atk_minus_def
    "bonus_by_stars": {
        "1": 0.01,
        "2": 0.02,
        "3": 0.03,
        "4": 0.04,
        "5": 0.05,
        "6": 0.06,
        "7": 0.07,
        "10": 0.10
    },
    "critical_pool": [1, 1, 1, 2, 3],
    "deck_root": "assets/img/decks",
    "setup_path": "modules/stage_setup.json",
    "nivel": "nivel_1",
    "deck_requirements": {}
}


def cargar_config(config_path=None) -> Dict[str, object]:
    if not config_path:
        config_path = DEFAULT_CONFIG.get("setup_path")
    path = Path(config_path)
    if not path.exists():
        return DEFAULT_CONFIG.copy()
    try:
        with open(path, "r", encoding="utf-8") as file:
            loaded = json.load(file)
        merged = DEFAULT_CONFIG.copy()
        merged.update(loaded)
        return merged
    except Exception:
        return DEFAULT_CONFIG.copy()


def sumar_stats(deck: Deck) -> Dict[str, int]:
    return {
        "hp": int(sum(card.get("hp", 0) for card in deck)),
        "atk": int(sum(card.get("atk", 0) for card in deck)),
        "def": int(sum(card.get("def", 0) for card in deck)),
    }


def armar_player(name: str, deck: Deck) -> PlayerState:
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


def parse_card_filename(file_path: Path) -> Card:
    name_no_ext = file_path.stem
    parts = name_no_ext.split("_")
    # formato esperado: <pos>_HP_<hp>_ATK_<atk>_DEF_<def>_<stars>
    hp = atk = defense = stars = 0
    try:
        hp = int(parts[2]) if len(parts) > 2 else 0
        atk = int(parts[4]) if len(parts) > 4 else 0
        defense = int(parts[6]) if len(parts) > 6 else 0
        stars = int(parts[7]) if len(parts) > 7 else 1
    except Exception:
        stars = 1
    return {
        "name": name_no_ext,
        "hp": hp,
        "atk": atk,
        "def": defense,
        "stars": stars,
        "image_path": str(file_path)
    }


def cargar_cartas_carpeta(folder: Path) -> List[Card]:
    cards = []
    for file in folder.glob("*.png"):
        cards.append(parse_card_filename(file))
    return cards


def elegir_cartas_random(folder: Path, cantidad: int) -> List[Card]:
    cartas = cargar_cartas_carpeta(folder)
    if cantidad > len(cartas):
        cantidad = len(cartas)
    return random.sample(cartas, cantidad)


def construir_mazo(deck_root: Path, cantidades: Dict[str, int]) -> Deck:
    mazo: Deck = []
    for folder_name, qty in cantidades.items():
        folder_path = deck_root / folder_name
        if folder_path.exists() and folder_path.is_dir():
            mazo.extend(elegir_cartas_random(folder_path, qty))
    random.shuffle(mazo)
    return mazo


def iniciar_stage(config_path=None, preset_config=None) -> Dict[str, object]:
    config = preset_config if preset_config is not None else cargar_config(config_path)
    nivel = config.get("nivel", "nivel_1")
    deck_root = Path(config.get("deck_root", DEFAULT_CONFIG["deck_root"]))

    requisitos = config.get("deck_requirements") or config.get(nivel, {}).get("cantidades", {})
    if not requisitos:
        requisitos = DEFAULT_CONFIG.get("deck_requirements", {})

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
        "finished_reason": ""
    }


def reiniciar_stage(stage: Dict[str, object]) -> None:
    config = stage.get("config", DEFAULT_CONFIG)
    new_stage = iniciar_stage(None, preset_config=config)
    stage.clear()
    stage.update(new_stage)


def mezclar_mazos(player: PlayerState, enemy: PlayerState) -> None:
    random.shuffle(player["deck"])
    random.shuffle(enemy["deck"])


def robar_cartas(player: PlayerState, enemy: PlayerState):
    if not player["deck"] or not enemy["deck"]:
        return None, None
    p_card = player["deck"].pop(0)
    e_card = enemy["deck"].pop(0)
    player["last_card"] = p_card
    enemy["last_card"] = e_card
    player["discard"].append(p_card)
    enemy["discard"].append(e_card)
    return p_card, e_card


def ataque_carta_con_bonus(card: Card, bonus_map: Dict[str, float]) -> float:
    stars = int(card.get("stars", 1))
    bonus_pct = card.get("bonus", bonus_map.get(str(stars), 0))
    return card.get("atk", 0) * (1 + bonus_pct)


def stats_carta_con_bonus(card: Card, bonus_map: Dict[str, float], crit_multiplier: int) -> Dict[str, int]:
    stars = int(card.get("stars", 1))
    bonus_pct = card.get("bonus", bonus_map.get(str(stars), 0))
    return {
        "hp": int(card.get("hp", 0) * (1 + bonus_pct) * crit_multiplier),
        "atk": int(card.get("atk", 0) * (1 + bonus_pct) * crit_multiplier),
        "def": int(card.get("def", 0) * (1 + bonus_pct) * crit_multiplier)
    }


def elegir_critico(multiplier_pool: List[int]) -> int:
    return random.choice(multiplier_pool or [1, 1, 2])


def aplicar_danio(target: PlayerState, damage: Dict[str, int]) -> None:
    for stat in ("hp", "atk", "def"):
        target["stats"][stat] = max(0, int(target["stats"].get(stat, 0) - damage.get(stat, 0)))


def aplicar_heal(player: PlayerState) -> None:
    player["stats"] = player.get("base_stats", {}).copy()
    player["heal_available"] = False


def activar_shield(player: PlayerState) -> None:
    player["shield_on"] = True
    player["shield_available"] = False


def calcular_puntaje(player_wins: bool, winner_card: Card, loser_card: Card, mode: str, fixed_points: int) -> int:
    if mode == "atk_minus_def":
        return max(10, int(winner_card.get("atk", 0) - loser_card.get("def", 0)))
    return int(fixed_points)


def resolver_mano(player: PlayerState, enemy: PlayerState, config: Dict[str, object]) -> Dict[str, object]:
    bonus_map = config.get("bonus_by_stars", {})
    crit_pool = config.get("critical_pool", [1, 1, 2])
    points_mode = config.get("points_mode", "fixed")
    points_per_hand = int(config.get("points_per_hand", 100))

    p_card, e_card = robar_cartas(player, enemy)
    if not p_card or not e_card:
        return {"finished": True, "reason": "deck_empty"}

    p_attack = ataque_carta_con_bonus(p_card, bonus_map)
    e_attack = ataque_carta_con_bonus(e_card, bonus_map)

    crit = elegir_critico(crit_pool)
    player_wins = p_attack >= e_attack
    winner = player if player_wins else enemy
    loser = enemy if player_wins else player
    winner_card = p_card if player_wins else e_card

    mirror_damage = loser.get("shield_on", False)
    if mirror_damage:
        loser["shield_on"] = False

    damage_target = loser if not mirror_damage else winner
    damage_stats = stats_carta_con_bonus(winner_card, bonus_map, crit)
    aplicar_danio(damage_target, damage_stats)

    score_gain = calcular_puntaje(
        player_wins=player_wins,
        winner_card=winner_card,
        loser_card=e_card if player_wins else p_card,
        mode=points_mode,
        fixed_points=points_per_hand
    )
    if player_wins:
        player["score"] += score_gain
    else:
        enemy["score"] += score_gain

    return {
        "finished": False,
        "crit": crit,
        "player_wins": player_wins,
        "mirror": mirror_damage,
        "p_card": p_card,
        "e_card": e_card,
        "damage": damage_stats,
        "score_gain": score_gain
    }


def chequear_fin_partida(player: PlayerState, enemy: PlayerState, time_left_ms: int) -> Tuple[bool, str]:
    if player["stats"]["hp"] <= 0:
        return True, "player_hp_zero"
    if enemy["stats"]["hp"] <= 0:
        return True, "enemy_hp_zero"
    if time_left_ms <= 0:
        return True, "time_over"
    if (not player["deck"] or not enemy["deck"]) and player["stats"]["hp"] != enemy["stats"]["hp"]:
        return True, "deck_empty"
    return False, ""


def tic_del_stage(stage: Dict[str, object], delta_ms: int) -> Tuple[bool, str]:
    stage["time_left_ms"] = max(0, int(stage.get("time_left_ms", 0) - delta_ms))
    finished, reason = chequear_fin_partida(stage["player"], stage["enemy"], stage["time_left_ms"])
    if finished:
        stage["finished"] = True
        stage["finished_reason"] = reason
    return finished, reason
