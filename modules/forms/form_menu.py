# ---- Imports ----
import pygame as py
import modules.forms.form_base as base_form
from utn_fra.pygame_widgets import (Label, Button)
import modules.variables as var
import sys


# --- Funciones ---
def create_menu_form(dict_form_data: dict) -> dict:
    """
    Usando el form que tenemos de base, crea el form (pantalla) del menu
    principal del juego
    """
    form = base_form.create_base_form(dict_form_data)

    form['lbl_titulo'] = Label(
        x = var.DIMENSION_PANTALLA[0]//2 - 250, y = 100,
        text = 'Menu principal', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 45,
        color = py.Color('black')
        )

    form['btn_play'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2 - 250, y = 150,
        text = 'Jugar', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('black'),
        on_click = imprimir_texto_boton, on_click_param = None
    )

    form['btn_ranking'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2 - 250, y = 200,
        text = 'Rankings', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('black'),
        on_click = base_form.cambiar_pantalla, 
        on_click_param = 'form_ranking'
    )

    form['btn_exit'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2 - 250, y = 300,
        text = 'Salir', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('black'),
        on_click = quit_game, on_click_param = None
    )


    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('btn_play'),
        form.get('btn_ranking'),
        form.get('btn_exit')
    ]
    
    var.dict_forms_status[form.get('name')] = form #Agregamos el formulario al diccionario en variables
    
    return form



def quit_game(_):
    print("Saliendo del juego con el botón.")
    py.quit()
    sys.exit()

def imprimir_texto_boton(_):
    print("Estamos presionando el boton 'JUGAR'")

def draw(dict_form_data: dict):
    """
    Dibuja
    """
    base_form.draw(dict_form_data)
    base_form.draw_widgets(dict_form_data)





def event_handler():
    """
    Verifica si está clickeando con el mouse, y en caso de que si, devuelve
    posicion
    """
    events = py.event.get()

    for event in events:
        if event.type == py.MOUSEBUTTONDOWN:
            print(f'coordenada mouse: {event.pos}')

def update(dict_form_data:dict):
    """
    Actualiza
    """
    event_handler() 
    base_form.update_widget(dict_form_data)
    

