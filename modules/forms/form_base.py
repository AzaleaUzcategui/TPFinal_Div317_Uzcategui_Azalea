# ---- Imports ----
import pygame as py
import modules.variables as var

def create_base_form(dict_form_data: dict) -> dict: 
    """
    Funcion que nos ayuda creando un formulario base que tiene toda la información
    básica que deben tener los formularios.
    """
    form = {}

    form['name'] = dict_form_data.get('name')
    form['screen'] = dict_form_data.get('screen')
    form['active'] = dict_form_data.get('active')
    form['x_coord'] = dict_form_data.get('coords')[0]
    form['y_coord'] = dict_form_data.get('coords')[1]

    form['music_path'] = dict_form_data.get('music_path')
    form['surface'] = py.image.load(dict_form_data.get('background')).convert_alpha()
    form['surface'] = py.transform.scale(form.get('surface'), dict_form_data.get('screen_dimensions'))

    form['rect'] = form.get('surface').get_rect()
    form['rect'].x = dict_form_data.get('coords')[0]
    form['rect'].y = dict_form_data.get('coords')[1]


    return form


# --- Creamos funciones comunes ----


def cambiar_pantalla(form_name: dict):
    """
    Setea a active el formulario a elección, para poder cambiar de
    pantalla.
    """
    set_active(form_name)



def draw_widgets (form_data:dict) -> dict:
    """
    Itera sobre los widgets (lista creada en cada formulario) y los muestra en pantalla
    """
    for widget in form_data.get('widgets_list'):
        widget.draw()



def update_widget (form_data:dict) -> dict:
    """
    Itera sobre los widgets (lista creada en cada formulario) y los actualiza, en este caso
    """
    for widget in form_data.get('widgets_list'):
        widget.update()


def update(form_data):
    """
    Caprichito
    """
    update_widget(form_data)



def set_active (form_name: str):
    """
    Activa el formulario que se le pasa por parametro
    """
    for form_n in var.dict_forms_status.keys():
        if form_n != form_name:
            var.dict_forms_status[form_n]['active'] = False
        else:
            var.dict_forms_status[form_n]['active'] = True


def draw(form_data: dict):
    """
    Fusiona la surface y el rectangulo del formulario en la pantalla.
    """
    form_data['screen'].blit(form_data.get('surface'), form_data.get('rect'))