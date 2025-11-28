# ---- Imports ----
import pygame as py
import modules.forms.form_base as base_form
from utn_fra.pygame_widgets import (Label, Button)
import modules.variables as var
import sys
import modules.stage as stage_logic
import modules.forms.form_stage as stage_form
import modules.sonido as sonido


# --- Funciones ---
def create_menu_form(dict_form_data: dict) -> dict:
    """
    Usando el form que tenemos de base, crea el form (pantalla) del menu
    principal del juego
    """
    form = base_form.create_base_form(dict_form_data)

    form['lbl_titulo'] = Label(
        x = var.DIMENSION_PANTALLA[0]//2, y = 150,
        text = 'Menu principal', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 55,
        color = py.Color('white')
        )

    form['btn_play'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2, y = 360,
        text = 'Jugar', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('white'),
        on_click = start_stage, on_click_param = None
    )

    form['btn_ranking'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2, y = 430,
        text = 'Rankings', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('white'),
        on_click = base_form.cambiar_pantalla, 
        on_click_param = 'form_ranking'
    )

    form['btn_opciones'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2, y = 500,
        text = 'Opciones', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('white'),
        on_click = base_form.cambiar_pantalla, 
        on_click_param = 'form_opciones'
    )

    form['btn_exit'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2, y = 575,
        text = 'Salir', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('white'),
        on_click = quit_game, on_click_param = None
    )
    


    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('btn_play'),
        form.get('btn_ranking'),
        form.get('btn_opciones'),
        form.get('btn_exit')
    ]
    
    var.dict_forms_status[form.get('name')] = form #Agregamos el formulario al diccionario en variables
    
    return form



def quit_game(_):
    print("Saliendo del juego con el boton.")
    py.quit()
    sys.exit()


def draw(dict_form_data: dict):
    """
    Dibuja
    """
    base_form.draw(dict_form_data)
    base_form.draw_widgets(dict_form_data)



def event_handler():
    """
    Verifica si esta clickeando con el mouse, y en caso de que si, devuelve
    posicion
    """
    events = py.event.get()

    for event in events:
        if event.type == py.MOUSEBUTTONDOWN:
            sonido.play_click()
            print(f'coordenada mouse: {event.pos}')
        

def update(dict_form_data:dict):
    """
    Actualiza
    """
    event_handler() 
    base_form.update_widget(dict_form_data)

    if not dict_form_data.get('music_config').get('music_init'):
        base_form.music_on(dict_form_data)
        dict_form_data['music_config']['music_init'] = True
    

def start_stage(_):
    """
    Resetea el stage y entra a la pantalla de juego.
    """
    stage = var.dict_forms_status.get('form_stage')
    if stage:
        stage_logic.reiniciar_stage(stage['stage'])
        stage['last_tick'] = py.time.get_ticks()
        stage_form.update_stats_labels(stage)
        stage['stage']['score_sent'] = False
    base_form.cambiar_pantalla('form_stage')
