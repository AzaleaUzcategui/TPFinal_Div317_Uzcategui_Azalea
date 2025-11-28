# ---- Imports ----
import pygame as py
import modules.forms.form_base as base_form
from utn_fra.pygame_widgets import (Label, Button)
import modules.variables as var
import modules.stage as stage_logic
import modules.forms.form_stage as stage_form



# --- Funciones ---
def create_pause_form(dict_form_data: dict) -> dict:
    """
    Usando el form que tenemos de base, crea el form (pantalla) del pausa.
    """
    form = base_form.create_base_form(dict_form_data)

    form['lbl_titulo'] = Label(
        x = var.DIMENSION_PANTALLA[0]//2, y = 100,
        text = 'Juego pausado', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 60,
        color = py.Color('white')
        )
    
    form['lbl_subtitulo'] = Label(
        x = var.DIMENSION_PANTALLA[0]//2, y = 160,
        text = 'El reloj se ha detenido', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 25,
        color = py.Color('white')
        )
    
    form['btn_restart'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2, y = 310,
        text = 'Restart', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('white'),
        on_click = restart_stage_from_pause, on_click_param = None
    )

    form['btn_resume'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2, y = 380,
        text = 'Resume', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('white'),
        on_click = resume_stage, on_click_param = None
    )

    form['btn_menu'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2, y = 450,
        text = 'Menu', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('white'),
        on_click = base_form.cambiar_pantalla, on_click_param = 'form_menu'
    )

    var.dict_forms_status[form.get('name')] = form

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitulo'),
        form.get('btn_restart'),
        form.get('btn_restart'),
        form.get('btn_resume'),
        form.get('btn_menu')
    ]

    return form


def draw(form_dict_data: dict):
    """
    draw
    """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)

def update(form_dict_data: dict):
    """
    update
    """
    base_form.update(form_dict_data)


def restart_stage_from_pause(_):
    stage = var.dict_forms_status.get('form_stage')
    if stage:
        stage_logic.reiniciar_stage(stage['stage'])
        stage['last_tick'] = py.time.get_ticks()
        stage_form.update_stats_labels(stage)
    base_form.cambiar_pantalla('form_stage')


def resume_stage(_):
    stage = var.dict_forms_status.get('form_stage')
    if stage:
        stage['last_tick'] = py.time.get_ticks()  # resetea el delta al volver
    base_form.cambiar_pantalla('form_stage')
