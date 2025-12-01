# ---- Stage form ----
import pygame as py
from pathlib import Path
from utn_fra.pygame_widgets import Label, ButtonImage
import modules.forms.form_base as base_form
import modules.variables as var
import modules.stage as stage_logic
import modules.sonido as sonido


def create_stage_form(dict_form_data: dict) -> dict:
    form = base_form.create_base_form(dict_form_data)

    form['stage'] = stage_logic.iniciar_stage(dict_form_data.get('config_path'))
    form['stage']['score_sent'] = False
    form['last_tick'] = py.time.get_ticks()
    form['enter_time'] = py.time.get_ticks()  
    form['pause_locked'] = False
    form['card_faces'] = {"player": None, "cpu": None}
    form['card_backs'] = {"player": None, "cpu": None}

    form['snd_mano'] = sonido.cargar_sonido(var.SND_MANO_GANADA, var.MANO_GANADA_VOLUMEN)

    centro_x = var.DIMENSION_PANTALLA[0] // 2

    form['lbl_timer'] = Label(
        x=centro_x, y=30,
        text='Tiempo: 0', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=28, color=py.Color('white')
    )

    form['lbl_score'] = Label(
        x=120, y=30,
        text='Puntaje: 0', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=28, color=py.Color('white')
    )

    # Stats individuales
    form['lbl_player_hp'] = Label(
        x=170, y=505,
        text='HP: 0', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=25, color=py.Color('black')
    )
    form['lbl_player_atk'] = Label(
        x=170, y=530,
        text='ATK: 0', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=18, color=py.Color('black')
    )
    form['lbl_player_def'] = Label(
        x=170, y=555,
        text='DEF: 0', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=18, color=py.Color('black')
    )

    form['lbl_enemy_hp'] = Label(
        x=170, y=180,
        text='HP: 0', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=25, color=py.Color('black')
    )
    form['lbl_enemy_atk'] = Label(
        x=170, y=205,
        text='ATK: 0', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=18, color=py.Color('black')
    )
    form['lbl_enemy_def'] = Label(
        x=170, y=230,
        text='DEF: 0', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=18, color=py.Color('black')
    )


    # Botones con imagenes >:C
    form['btn_play'] = ButtonImage(
        x=935, y=375,
        width= 100, height=35,
        text='Jugar mano', screen=form.get('screen'),
        image_path=var.PLAY_BTN, font_size=32,
        on_click=play_hand, on_click_param=form
    )

    form['btn_heal'] = ButtonImage(
        x=940, y=570,
        width= 100, height=35,
        text='', screen=form.get('screen'),
        image_path=var.HEAL_BTN, font_size=26,
        on_click=use_heal, on_click_param=form
    )

    form['btn_shield'] = ButtonImage(
        x=940, y=610,
        width= 100, height=35,
        text='', screen=form.get('screen'),
        image_path=var.SHIELD_BTN, font_size=26,
        on_click=use_shield, on_click_param=form
    )

    form['widgets_list'] = [
        form.get('lbl_timer'), form.get('lbl_score'),
        form.get('lbl_player_hp'), form.get('lbl_player_atk'), form.get('lbl_player_def'),
        form.get('lbl_enemy_hp'), form.get('lbl_enemy_atk'), form.get('lbl_enemy_def'),
        form.get('btn_play'), form.get('btn_heal'),
        form.get('btn_shield')
    ]


    

    var.dict_forms_status[form.get('name')] = form
    update_stats_labels(form)
    update_card_surfaces(form, None, None)
    return form


def update_stats_labels(form: dict) -> None:
    """
    Refresca kas stats, timer, puntaje

    Muestra los botones de heal y shield hasta que se utilicen
    """
    stage = form.get('stage')
    player = stage.get('player')
    enemy = stage.get('enemy')
    time_left = max(0, stage.get('time_left_ms', 0) // 1000)

    form.get('lbl_timer').update_text(text=f'Tiempo: {time_left}s', color=py.Color('white'))
    form.get('lbl_score').update_text(text=f"Puntaje: {player.get('score', 0)}", color=py.Color('white'))

    form.get('lbl_player_hp').update_text(text=f"HP: {player.get('stats', {}).get('hp', 0)}", color=py.Color('black'))
    form.get('lbl_player_atk').update_text(text=f"ATK: {player.get('stats', {}).get('atk', 0)}", color=py.Color('black'))
    form.get('lbl_player_def').update_text(text=f"DEF: {player.get('stats', {}).get('def', 0)}", color=py.Color('black'))

    form.get('lbl_enemy_hp').update_text(text=f"HP: {enemy.get('stats', {}).get('hp', 0)}", color=py.Color('black'))
    form.get('lbl_enemy_atk').update_text(text=f"ATK: {enemy.get('stats', {}).get('atk', 0)}", color=py.Color('black'))
    form.get('lbl_enemy_def').update_text(text=f"DEF: {enemy.get('stats', {}).get('def', 0)}", color=py.Color('black'))

    btn_heal = form.get("btn_heal")
    btn_shield = form.get("btn_shield")

    if player.get("heal_available"):
        if btn_heal not in form['widgets_list']:
            form['widgets_list'].append(btn_heal)
    else:
        if btn_heal in form['widgets_list']:
            form['widgets_list'].remove(btn_heal)

    if player.get("shield_available"):
        if btn_shield not in form['widgets_list']:
            form['widgets_list'].append(btn_shield)
    else:
        if btn_shield in form['widgets_list']:
            form['widgets_list'].remove(btn_shield)

def load_and_scale(image_path: str, size=(140, 200)) -> py.Surface:
    """
    Carga y escala la imagen
    """
    surf = py.image.load(image_path).convert_alpha()
    return py.transform.smoothscale(surf, size) #Lo tuve que buscar


def back_surface(deck_name: str, config: dict, size=(140, 200)) -> py.Surface:
    """
    Intenta cargar el reverso real del mazo (archivo que contenga 'reverse' en el nombre).
    Si no existe, devuelve un rectángulo negro
    """
    deck_root = Path(config.get("deck_root", "assets/img/decks"))
    deck_folder = deck_root / deck_name
    reverse_file = None
    if deck_folder.exists():
        for file in deck_folder.glob("*reverse*.png"):
            reverse_file = file
            break
    if reverse_file:
        return load_and_scale(str(reverse_file), size)

    # placeholder negro
    surf = py.Surface(size)
    surf.fill(py.Color('black'))
    return surf


def update_card_surfaces(form: dict, p_card: dict | None, e_card: dict | None):
    """
    Actualiza las surfaces de cartas (caras y reversos).
    """
    if p_card:
        form['card_faces']['player'] = load_and_scale(p_card.get('image_path'))
    if e_card:
        form['card_faces']['cpu'] = load_and_scale(e_card.get('image_path'))

    # Reversos: proxima carta del mazo si existe
    stage_data = form.get('stage')
    p_next = stage_data['player']['deck'][0] if stage_data['player']['deck'] else None
    e_next = stage_data['enemy']['deck'][0] if stage_data['enemy']['deck'] else None

    config = stage_data.get('config', {})
    form['card_backs']['player'] = back_surface(p_next.get('deck'), config) if p_next else None
    form['card_backs']['cpu'] = back_surface(e_next.get('deck'), config) if e_next else None


def draw_cards(form: dict):
    """
    Dibuja reversos y cartas jugadas en pantalla.
    """
    screen = form.get('screen')
    card_w, card_h = 140, 200

    # CPU
    back_cpu = form['card_backs'].get('cpu')
    if back_cpu:
        screen.blit(back_cpu, (300, 110))
    face_cpu = form['card_faces'].get('cpu')
    if face_cpu:
        screen.blit(face_cpu, (520, 110))

    # Player
    back_player = form['card_backs'].get('player')
    if back_player:
        screen.blit(back_player, (300, 450))
    face_player = form['card_faces'].get('player')
    if face_player:
        screen.blit(face_player, (520, 450))


def reset_stage_state(form: dict):
    stage_logic.reiniciar_stage(form['stage'])
    form['stage']['score_sent'] = False
    form['last_tick'] = py.time.get_ticks()
    form['enter_time'] = py.time.get_ticks()
    update_stats_labels(form)
    update_card_surfaces(form, None, None)
    form.get('lbl_last_result').update_text(text='Listo para jugar la primera mano', color=py.Color('white'))


def play_hand(form: dict):
    stage = form.get('stage')
    if stage.get('finished'):
        return
    if py.time.get_ticks() - form.get('enter_time', 0) < 250:
        return
    result = stage_logic.resolver_mano(stage['player'], stage['enemy'], stage['config'])
    if result.get('finished'):
        update_stats_labels(form)
        finalizar_stage(form, result.get('reason'))
        return

    msg = 'Ganaste la mano' if result.get('player_wins') else 'Perdiste la mano'
    if result.get('mirror'):
        msg += ' (SHIELD activo)'
    if result.get('crit', 1) > 1:
        msg += f" | Critico x{result.get('crit')}"
    msg += f" | +{result.get('score_gain')} pts"

    if result.get('player_wins') and form.get('snd_mano'):
        form['snd_mano'].play()
    update_stats_labels(form)
    update_card_surfaces(form, result.get('p_card'), result.get('e_card'))

    finished, reason = stage_logic.chequear_fin_partida(stage['player'], stage['enemy'], stage['time_left_ms'])
    if finished:
        finalizar_stage(form, reason)


def use_heal(form: dict):
    stage = form.get('stage')
    player = stage.get('player')
    if stage.get('finished') or not player.get('heal_available'):
        return
    stage_logic.aplicar_heal(player)
    update_stats_labels(form)


def use_shield(form: dict):
    stage = form.get('stage')
    player = stage.get('player')
    if stage.get('finished') or not player.get('shield_available'):
        return
    stage_logic.activar_shield(player)
    update_stats_labels(form)


def restart_stage(form: dict):
    reset_stage_state(form)


def draw(form_dict_data: dict):
    base_form.draw(form_dict_data)
    draw_cards(form_dict_data)
    base_form.draw_widgets(form_dict_data)


def update(form_dict_data: dict):
    keys = py.key.get_pressed()
    if keys[py.K_ESCAPE]:
        if not form_dict_data.get('pause_locked', False):
            form_dict_data['last_tick'] = py.time.get_ticks()
            base_form.cambiar_pantalla('form_pause')
            form_dict_data['pause_locked'] = True
    else:
        form_dict_data['pause_locked'] = False

    now = py.time.get_ticks()
    delta = now - form_dict_data.get('last_tick', now)
    form_dict_data['last_tick'] = now

    stage_data = form_dict_data.get('stage')
    if not stage_data.get('finished'):
        finished, reason = stage_logic.tic_del_stage(stage_data, delta)
        if finished:
            finalizar_stage(form_dict_data, reason)

    update_stats_labels(form_dict_data)
    base_form.update(form_dict_data)


def determinar_ganador(player: dict, enemy: dict) -> str:
    if player['stats']['hp'] > enemy['stats']['hp']:
        return "Ganaste"
    if player['stats']['hp'] < enemy['stats']['hp']:
        return "Gano la CPU"
    return "Empate"


def finalizar_stage(form: dict, reason: str):
    """
    Marca fin de partida y envÃ­a al form_nombre con puntaje y resultado.
    """
    stage = form.get('stage')
    stage['finished'] = True
    stage['finished_reason'] = reason

    if not stage.get('score_sent', False):
        stage['score_sent'] = True
        form_nombre = var.dict_forms_status.get('form_nombre')
        if form_nombre:
            score_player = stage['player']['score']
            resultado = determinar_ganador(stage['player'], stage['enemy'])
            form_nombre['last_score'] = score_player
            form_nombre['lbl_score'].update_text(text=f"Puntaje: {score_player}", color=py.Color('white'))
            form_nombre['input_text'] = ""
            form_nombre['lbl_input'].update_text(text='Nombre: ', color=py.Color('white'))
            form_nombre['lbl_resultado'].update_text(text=resultado, color=py.Color('white'))
            base_form.cambiar_pantalla('form_nombre')


