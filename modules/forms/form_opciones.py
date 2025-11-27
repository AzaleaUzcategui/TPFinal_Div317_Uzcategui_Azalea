# ---- Imports ----
import pygame as py
import modules.forms.form_base as base_form
from utn_fra.pygame_widgets import (Label, Button)
import modules.variables as var
import modules.sonido as sonido


# --- Funciones ---
def create_opciones_form(dict_form_data: dict) -> dict:
    """
    Usando el form que tenemos de base, crea el form (pantalla) de las opciones
    del juego
    """
    form = base_form.create_base_form(dict_form_data)
    

    form['lbl_titulo'] = Label(
        x = var.DIMENSION_PANTALLA[0]//2, y = 75,
        text = 'Opciones', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 45,
        color = py.Color('white')
        )

    form['btn_on'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2 - 120, y = 130,
        text = 'music on', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 30,
        color = py.Color('white'),
        on_click = activar_musica, on_click_param = form
        )

    form['btn_off'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2 + 120, y = 130,
        text = 'music off', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 30,
        color = py.Color('white'),
        on_click =desactivar_musica, on_click_param = form
        )

    form['btn_down'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2 - 70, y = 190,
        text = '<', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('white'),
        on_click = modificar_volumen, on_click_param = - 10
    )

    form['btn_up'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2 + 70, y = 190,
        text = '>', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('white'),
        on_click = modificar_volumen, on_click_param = 10
    )

    form['lbl_vol'] = Label(
        x = var.DIMENSION_PANTALLA[0]//2, y = 190,
        text = f'{sonido.get_actual_volume()}', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 30,
        color = py.Color('white')
        )

    form['btn_volver'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2, y = 345,
        text = 'Volver', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('white'),
        on_click = base_form.cambiar_pantalla, on_click_param = 'form_menu'
    )


    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('btn_on'),
        form.get('btn_off'),
        form.get('btn_down'),
        form.get('btn_up'),
        form.get('lbl_vol'),
        form.get('btn_volver')
    ]
    
    var.dict_forms_status[form.get('name')] = form #Agregamos el formulario al diccionario en variables
    
    return form


def modificar_volumen(volumen: int):
    """
    Dado un volumen, se suma o resta ese mismo al volumen actual
    """

    vol_actual = sonido.get_actual_volume()
    if (vol_actual > 0 and volumen < 0) or\
        (vol_actual < 100 and volumen > 0):
        vol_actual += volumen
        sonido.set_volume(vol_actual)
    


def activar_musica(form_dict_data: dict):
    """
    Activo musica
    """
    form_dict_data['music_config']['music_on'] = True
    base_form.music_on(form_dict_data)

def desactivar_musica(form_dict_data:dict):
    """
    Desactivo musica
    """
    form_dict_data['music_config']['music_on'] = False
    sonido.stop_music()


def draw(form_dict_data: dict):
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)

def update(form_dict_data: dict):
    lbl_vol: Label = form_dict_data.get('widgets_list')[5]
    lbl_vol.update_text(text=f'{sonido.get_actual_volume()}', color=py.Color('white'))
    base_form.update(form_dict_data)


