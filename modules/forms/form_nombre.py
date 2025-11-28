# ---- Imports ----
import pygame as py
from utn_fra.pygame_widgets import Label, Button
import modules.forms.form_base as base_form
import modules.variables as var


def create_nombre_form(dict_form_data: dict) -> dict:
    form = base_form.create_base_form(dict_form_data)

    form['input_text'] = ""
    form['max_chars'] = 12
    form['last_score'] = 0

    form['lbl_titulo'] = Label(
        x=var.DIMENSION_PANTALLA[0]//2, y=140,
        text='Ingresa tu nombre', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=42,
        color=py.Color('white')
    )

    form['lbl_score'] = Label(
        x=var.DIMENSION_PANTALLA[0]//2, y=200,
        text='Puntaje: 0', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=30,
        color=py.Color('white')
    )

    form['lbl_resultado'] = Label(
        x=var.DIMENSION_PANTALLA[0]//2, y=230,
        text='', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=26,
        color=py.Color('white')
    )

    form['lbl_input'] = Label(
        x=var.DIMENSION_PANTALLA[0]//2, y=260,
        text='Nombre: ', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=28,
        color=py.Color('white')
    )

    form['btn_guardar'] = Button(
        x=var.DIMENSION_PANTALLA[0]//2 - 100, y=340,
        text='Guardar', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=32,
        color=py.Color('white'),
        on_click=guardar_nombre, on_click_param=form
    )

    form['btn_cancelar'] = Button(
        x=var.DIMENSION_PANTALLA[0]//2 + 100, y=340,
        text='Cancelar', screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD, font_size=32,
        color=py.Color('white'),
        on_click=base_form.cambiar_pantalla, on_click_param='form_menu'
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_score'),
        form.get('lbl_resultado'),
        form.get('lbl_input'),
        form.get('btn_guardar'),
        form.get('btn_cancelar')
    ]

    var.dict_forms_status[form.get('name')] = form
    return form


def set_puntaje(form: dict, puntaje: int):
    form['last_score'] = puntaje
    form['lbl_score'].update_text(text=f'Puntaje: {puntaje}', color=py.Color('white'))
    form['input_text'] = ""
    form['lbl_input'].update_text(text='Nombre: ', color=py.Color('white'))


def set_resultado(form: dict, texto: str):
    """
    UPdateo el lbl
    """
    form['lbl_resultado'].update_text(text=texto, color=py.Color('white'))


def guardar_nombre(form: dict):
    nombre = form.get('input_text', "").strip()
    if not nombre:
        nombre = "Anon"
    puntaje = form.get('last_score', 0)
    # append al csv
    with open(var.RANKING_CSV, 'a', encoding='utf-8') as f:
        f.write(f"\n{nombre},{puntaje}")
    base_form.cambiar_pantalla('form_ranking')



def manejar_input(form: dict):
    for event in py.event.get():
        if event.type == py.KEYDOWN:
            if event.key == py.K_BACKSPACE:
                form['input_text'] = form.get('input_text', "")[:-1]
            elif event.key == py.K_RETURN:
                guardar_nombre(form)
            else:
                char = event.unicode
                if char.isprintable() and len(form.get('input_text', "")) < form.get('max_chars', 12):
                    form['input_text'] = form.get('input_text', "") + char
        elif event.type == py.MOUSEBUTTONDOWN:
            pass  

    
    form['lbl_input'].update_text(text=f"Nombre: {form.get('input_text', '')}", color=py.Color('white'))


def draw(form_dict_data: dict):
    """
    DRAW
    """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)


def update(form_dict_data: dict):
    """
    UPDATE (brote psicotico)
    """
    manejar_input(form_dict_data)
    base_form.update(form_dict_data)
