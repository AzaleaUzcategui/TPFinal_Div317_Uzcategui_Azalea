# ---- Imports ----
import pygame as py
import modules.forms.form_menu as menu_form
import modules.forms.form_rankings as ranking_form
import modules.forms.form_opciones as options_form
import modules.forms.form_pause as pause_form
import modules.forms.form_stage as stage_form
import modules.variables as var
from utn_fra.pygame_widgets import MousePointer


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
    controller['music_config'] = datos_juego.get('music_config')

    
    cursor_img = py.image.load(var.MOUSE_POINTER)
    size = cursor_img.get_size()
    half_size =(size[0] //10, size[1]//10)
    cursor_img = py.transform.scale(cursor_img, (half_size))

    controller['mouse_cursor'] = MousePointer(controller.get('main_screen'), cursor_img)
    controller['mouse_c'] = py.sprite.Group(controller.get('mouse_cursor'))



    # --- Lista de todos los formularios (pantallas) ----
    controller['forms_list'] = [
        menu_form.create_menu_form(
            {
             'name': 'form_menu',
             'screen': controller.get('main_screen'),
             'active': True,
             'coords': (0, 0),
             'music_path': var.MUSICA_MENU,
             'background': var.FONDO_MENU,
             'screen_dimensions': var.DIMENSION_PANTALLA,
             'music_config': controller.get('music_config')
            }
        ),
        ranking_form.create_ranking_form(
            {
             'name': 'form_ranking',
             'screen': controller.get('main_screen'),
             'active': False,
             'coords': (0, 0),
             'music_path': var.MUSICA_RANKING,
             'background': var.FONDO_RANKING,
             'screen_dimensions': var.DIMENSION_PANTALLA,
             'music_config': controller.get('music_config')
            }
        ),
        options_form.create_opciones_form(
            {
             'name': 'form_opciones',
             'screen': controller.get('main_screen'),
             'active': False,
             'coords': (0, 0),
             'music_path': var.MUSICA_OPCIONES,
             'background': var.FONDO_OPCIONES,
             'screen_dimensions': var.DIMENSION_PANTALLA,
             'music_config': controller.get('music_config')
            }
        ),
        pause_form.create_pause_form(
            {
             'name': 'form_pause',
             'screen': controller.get('main_screen'),
             'active': False,
             'coords': (0, 0),
            'music_path': var.MUSICA_PAUSA,
            'background': var.FONDO_PAUSA,
            'screen_dimensions': var.DIMENSION_PANTALLA,
            'music_config': controller.get('music_config')
            }
        ),
        stage_form.create_stage_form(
            {
             'name': 'form_stage',
             'screen': controller.get('main_screen'),
             'active': False,
             'coords': (0, 0),
             'music_path': var.MUSICA_STAGE,
             'background': var.FONDO_STAGE,
             'screen_dimensions': var.DIMENSION_PANTALLA,
             'music_config': controller.get('music_config'),
             'config_path': None
            }
        )
    ]

    return controller



def forms_update(form_controller: dict):
    """
    Actualiza el formulario activo
    """
    lista_formularios = form_controller.get('forms_list')

    for form in lista_formularios:

        if form.get('active'):
            match form.get('name'):
                case 'form_menu':
                #Formulario MENU
                    form_menu = lista_formularios[0]
                    menu_form.update(form_menu)
                    menu_form.draw(form_menu)
                case 'form_ranking':
                #Formulario RANKING
                    form_ranking = lista_formularios[1]
                    ranking_form.update(form_ranking)
                    ranking_form.draw(form_ranking)
                #Formulacio OPCIONES
                case 'form_opciones':
                    form_opciones = lista_formularios[2]
                    options_form.update(form_opciones)
                    options_form.draw(form_opciones)
                case 'form_pause':
                    form_pause = lista_formularios[3]
                    pause_form.update(form_pause)
                    pause_form.draw(form_pause)
                case 'form_stage':
                    form_stage = lista_formularios[4]
                    stage_form.update(form_stage)
                    stage_form.draw(form_stage)





def update(form_controller:dict):
    """
    Se fija que formulario está activo, con un nombre más sencillo para poder llamarlo luego con
    comodidad.
    """
    forms_update(form_controller)
    
    form_controller.get('mouse_c').update()
    form_controller.get('mouse_c').draw(form_controller.get('main_screen'))
