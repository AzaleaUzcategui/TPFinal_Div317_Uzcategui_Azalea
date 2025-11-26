# --- Imports ----
import pygame as py
import sys
import modules.forms.form_base as base_form
from utn_fra.pygame_widgets import (Label, Button)
import modules.variables as var



# --- Funciones ---
def create_ranking_form(dict_form_data: dict) -> dict:
    """
    En este caso, el formulario que se crea es el de ranking.
    """
    form = base_form.create_base_form(dict_form_data)
    
    form['lista_ranking_file'] = []

    form['lista_ranking_screen'] = []

    form['data_loaded'] = False #Para probar si la data está cargada

    form['lbl_titulo'] = Label(
        x = var.DIMENSION_PANTALLA[0]//2 - 50, y = 50,
        text = 'Dragon Ball Z || Trading card game', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 50,
        color = py.Color('white')
        )

    form['lbl_subtitulo'] = Label(
        x = var.DIMENSION_PANTALLA[0]//2 - 250, y = 120,
        text = 'Top 10 ranking', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 40,
        color = py.Color('white')
        )

    form['btn_volver'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2 - 250, y = 500,
        text = 'Volver', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 35,
        color = py.Color('white'),
        on_click = cambiar_formulario, on_click_param = [form, 'form_menu']
    )

    #Listita de wiches :3
    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitulo'),
        form.get('btn_volver')
    ]

    var.dict_forms_status[form.get('name')] = form 

    return form


def cambiar_formulario(param_list: list):
    """
    Setea a active el form elegido, y en este caso, cambia el valor del
    form_ranking['data_loaded']
    """
    form_ranking = param_list[0]
    form_name = param_list[1]

    print("Saliendo del form ranking")
    form_ranking['data_loaded'] = False
    base_form.cambiar_pantalla(form_name)


def draw (form_dict_data: dict):
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)
    #Widgets exclusivos de ranking.

def update(form_dict_data: dict):
    if form_dict_data.get('data_loaded') == True:
        pass
    base_form.update(form_dict_data)