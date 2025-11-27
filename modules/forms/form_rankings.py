# --- Imports ----
import pygame as py
import sys
import modules.forms.form_base as base_form
from utn_fra.pygame_widgets import (Label, Button)
import modules.variables as var
import modules.auxiliar as aux



# --- Funciones ---
def create_ranking_form(dict_form_data: dict) -> dict:
    """
    En este caso, el formulario que se crea es el de ranking.
    """
    form = base_form.create_base_form(dict_form_data)
    
    form['lista_ranking_file'] = []

    form['lista_ranking_screen'] = []

    form['data_loaded'] = False #Para probar si la data está cargada


    form['lbl_subtitulo'] = Label(
        x = var.DIMENSION_PANTALLA[0]//2, y = 100,
        text = 'Top 8 ranking', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 60,
        color = py.Color('white')
        )

    form['btn_volver'] = Button(
        x = var.DIMENSION_PANTALLA[0]//2, y = 595,
        text = 'Volver', screen = form.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 35,
        color = py.Color('white'),
        on_click = cambiar_formulario, on_click_param = [form, 'form_menu']
    )

    #Listita de wiches :3
    form['widgets_list'] = [
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
    form_ranking['lista_ranking_screen'] = []
    form_ranking['lista_ranking_file'] = []
    base_form.cambiar_pantalla(form_name)

def init_ranking(form_dict_data: dict):
    #form_dict_data['lista_ranking_screen'] = []
    matriz = form_dict_data.get('lista_ranking_file')

    posicion_y = var.DIMENSION_PANTALLA[1] //2 - 130

    for indice_fila in range(len(matriz)):
        fila = matriz[indice_fila]

        """
        POSICION         NOMBRE         SCORE
        POSICION         NOMBRE         SCORE
        POSICION         NOMBRE         SCORE
        
        """


        placement = Label(
        x = var.DIMENSION_PANTALLA[0]//2 - 100, y = posicion_y,
        text = f'{indice_fila + 1}_ ', screen = form_dict_data.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 30,
        color = py.Color('white')
        )
        name = Label(
        x = var.DIMENSION_PANTALLA[0]//2, y = posicion_y,
        text = f'{fila[0]}', screen = form_dict_data.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 25,
        color = py.Color('white')
        )
        score = Label(
        x = var.DIMENSION_PANTALLA[0]//2 + 100, y = posicion_y,
        text = f'---- {fila[1]}', screen = form_dict_data.get('screen'),
        font_path = var.FUENTE_ALAGARD, font_size = 25,
        color = py.Color('white')
        )


        posicion_y += 40

        form_dict_data['lista_ranking_screen'].append(placement)
        form_dict_data['lista_ranking_screen'].append(name)
        form_dict_data['lista_ranking_screen'].append(score)




def inicializar_ranking_archivo(form_dict_data: dict):
    """
    Abre el archivo y lee los primeros 10 jugadores.
    """
    if not form_dict_data.get('data_loaded'):
        form_dict_data['lista_ranking_file'] = aux.cargar_ranking(var.RANKING_CSV, top=8)
        init_ranking(form_dict_data)
        form_dict_data['data_load'] = True


def draw (form_dict_data: dict):
    """
    Dibuja widgets
    """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)
    #Widgets exclusivos de ranking.
    for widget in form_dict_data.get('lista_ranking_screen'):
        widget.draw()


def update(form_dict_data: dict):
    """
    Carga widgets
    """
    if not form_dict_data.get('data_loaded'):
        inicializar_ranking_archivo (form_dict_data)

    base_form.update(form_dict_data)