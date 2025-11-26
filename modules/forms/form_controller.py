# ---- Imports ----
import pygame as py
import modules.forms.form_menu as menu_form
import modules.forms.form_rankings as ranking_form
import modules.variables as var


# --- funciones ---
def create_form_controller(screen: py.Surface, datos_juego: dict):
    """
    Se crea el form que controlará las distintas pantallas del juego. Esta función
    se llama desde el módulo game.
    """

    controller = {}

    controller['main_screen'] = screen
    controller['current_stage'] = 1
    controller['game_started'] = False
    controller['player'] = datos_juego.get('player')
    controller['enemy'] = None



    # --- Lista de todos los formularios (pantallas) ----
    controller['forms_list'] = [
        menu_form.create_menu_form(
            {
             'name': 'form_menu',
             'screen': controller.get('main_screen'),
             'active': True,
             'coords': (0, 0),
             'music_path': '..',
             'background': var.FONDO_MENU,
             'screen_dimensions': var.DIMENSION_PANTALLA
            }
        ),
        ranking_form.create_ranking_form(
            {
             'name': 'form_ranking',
             'screen': controller.get('main_screen'),
             'active': False,
             'coords': (0, 0),
             'music_path': '..',
             'background': var.FONDO_RANKING,
             'screen_dimensions': var.DIMENSION_PANTALLA
            }
        )
    ]

    return controller



def forms_update(form_controller: dict):
    """
    Actualiza el formulario activo
    """
    lista_formularios = form_controller.get('forms_list')

    #Formulario MENU
    if lista_formularios[0].get('active'):
        form_menu = lista_formularios[0]
        menu_form.update(form_menu)
        menu_form.draw(form_menu)

    #Formulario RANKING
    elif lista_formularios[1].get('active'):
        form_ranking = lista_formularios[1]
        ranking_form.update(form_ranking)
        ranking_form.draw(form_ranking)


def update(form_controller:dict):
    """
    Se fija que formulario está activo, con un nombre más sencillo para poder llamarlo luego con
    comodidad.
    """
    forms_update(form_controller)