# ---- Stage form ----
import pygame as py
from utn_fra.pygame_widgets import Label, ButtonImage
import modules.forms.form_base as base_form
import modules.variables as var
import modules.stage as stage_logic


def create_stage_form(dict_form_data: dict) -> dict:
    form = base_form.create_base_form(dict_form_data)

    form['stage'] = stage_logic.iniciar_stage(dict_form_data.get('config_path'))
    form['last_tick'] = py.time.get_ticks()
    form['enter_time'] = py.time.get_ticks()  # evita disparar mano por el click anterior
    form['pause_locked'] = False

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

    form['lbl_player_stats'] = Label(
        x=180, y=480,
        text='Jugador', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=30, color=py.Color('black')
    )
    form['lbl_enemy_stats'] = Label(
        x=180, y=160,
        text='CPU', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=30, color=py.Color('black')
    )

    # Stats individuales
    form['lbl_player_hp'] = Label(
        x=170, y=505,
        text='HP: 0', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=18, color=py.Color('black')
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
        font_path=var.FUENTE_ALAGARD, font_size=18, color=py.Color('black')
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

    form['lbl_last_result'] = Label(
        x=70, y=375,
        text='Listo para jugar',
        screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=22, color=py.Color('red')
    )

    form['btn_play'] = ButtonImage(
        x=940, y=375,
        width=120, height=60,
        text='Jugar mano', screen=form.get('screen'),
        image_path=var.PLAY_BTN, font_size=32,
        on_click=play_hand, on_click_param=form
    )

    # Botones con imagenes
    form['btn_heal'] = ButtonImage(
        x=940, y=570,
        width=120, height=60,
        text='', screen=form.get('screen'),
        image_path=var.HEAL_BTN, font_size=26,
        on_click=use_heal, on_click_param=form
    )

    form['btn_shield'] = ButtonImage(
        x=940, y=630,
        width=120, height=60,
        text='', screen=form.get('screen'),
        image_path=var.SHIELD_BTN, font_size=26,
        on_click=use_shield, on_click_param=form
    )

    form['widgets_list'] = [
        form.get('lbl_timer'), form.get('lbl_score'),
        form.get('lbl_player_stats'), form.get('lbl_enemy_stats'),
        form.get('lbl_player_hp'), form.get('lbl_player_atk'), form.get('lbl_player_def'),
        form.get('lbl_enemy_hp'), form.get('lbl_enemy_atk'), form.get('lbl_enemy_def'),
        form.get('lbl_last_result'), form.get('btn_play'), form.get('btn_heal'),
        form.get('btn_shield')
    ]

    var.dict_forms_status[form.get('name')] = form
    update_stats_labels(form)
    return form


def update_stats_labels(form: dict) -> None:
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


def reset_stage_state(form: dict):
    stage_logic.reiniciar_stage(form['stage'])
    form['last_tick'] = py.time.get_ticks()
    form['enter_time'] = py.time.get_ticks()
    update_stats_labels(form)
    form.get('lbl_last_result').update_text(text='Listo para jugar la primera mano', color=py.Color('white'))


def play_hand(form: dict):
    stage = form.get('stage')
    if stage.get('finished'):
        return
    if py.time.get_ticks() - form.get('enter_time', 0) < 250:
        return

    result = stage_logic.resolver_mano(stage['player'], stage['enemy'], stage['config'])
    if result.get('finished'):
        stage['finished'] = True
        stage['finished_reason'] = result.get('reason')
        form.get('lbl_last_result').update_text(text='Sin cartas para seguir jugando', color=py.Color('white'))
        update_stats_labels(form)
        return

    msg = 'Ganaste la mano' if result.get('player_wins') else 'Perdiste la mano'
    if result.get('mirror'):
        msg += ' (SHIELD activo)'
    if result.get('crit', 1) > 1:
        msg += f" | Critico x{result.get('crit')}"
    msg += f" | +{result.get('score_gain')} pts"

    form.get('lbl_last_result').update_text(text=msg, color=py.Color('white'))
    update_stats_labels(form)

    finished, reason = stage_logic.chequear_fin_partida(stage['player'], stage['enemy'], stage['time_left_ms'])
    if finished:
        stage['finished'] = True
        stage['finished_reason'] = reason


def use_heal(form: dict):
    stage = form.get('stage')
    player = stage.get('player')
    if stage.get('finished') or not player.get('heal_available'):
        return
    stage_logic.aplicar_heal(player)
    form.get('lbl_last_result').update_text(text='HEAL usado: stats restaurados', color=py.Color('white'))
    update_stats_labels(form)


def use_shield(form: dict):
    stage = form.get('stage')
    player = stage.get('player')
    if stage.get('finished') or not player.get('shield_available'):
        return
    stage_logic.activar_shield(player)
    form.get('lbl_last_result').update_text(text='SHIELD activado: proximo golpe rebota', color=py.Color('white'))
    update_stats_labels(form)


def restart_stage(form: dict):
    reset_stage_state(form)


def draw(form_dict_data: dict):
    base_form.draw(form_dict_data)
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
            form_dict_data.get('lbl_last_result').update_text(text=f'Fin de partida: {reason}', color=py.Color('white'))

    update_stats_labels(form_dict_data)
    base_form.update(form_dict_data)
