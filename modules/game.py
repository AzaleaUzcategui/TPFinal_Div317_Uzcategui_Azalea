# ---- Imports ----
import pygame as py
import modules.variables as var
import sys
import modules.forms.form_controller as form_controller


# --- Game ---
def mi_jueguito ():
    """
    Esta función dibuja la pantalla original, el ícono y la caption. Inicializa pygame y los
    formularios

    """

    py.init()


    # ---- DISPLAY ----
    pantalla = py.display.set_mode((var.DIMENSION_PANTALLA))
    py.display.set_caption(var.TITULO)
    py.display.set_icon(var.ICONO_SURFACE)


    corriendo = True
    reloj = py.time.Clock()
    datos_juego = {
        "puntaje": 0,
        "cant_vidas": var.CANTIDAD_DE_VIDAS,
        "player": {},
        "music_config": {
            "music_volme": var.VOLUMEN_INICIAL,
            "music_on": True,
            "music_init": False #Musica inicializada
        }

    }



    # ----- Controlador ----
    form_control = form_controller.create_form_controller(pantalla, datos_juego)




    # ---- Bucle principal ----
    while corriendo:

        eventos = py.event.get()
        reloj.tick(var.FPS)

        for event in eventos:

            if event.type == py.QUIT:
                print("Cerrando el juego")
                corriendo = False
          

        form_controller.update(form_control)


        py.display.flip() #(update) es lo mismo
    
    py.quit()
    sys.exit()