# ---- Imports ----
import pygame as py
import modules.variables as var



# --- Game ---
def mi_jueguito ():

    py.init()


    # ---- DISPLAY ----
    pantalla = py.display.set_mode((var.dimension_pantalla))
    py.display.set_caption(var.titulo)
    py.display.set_icon(var.icono_surface)
    


    # ---- Bucle principal ----
    while True:
        for event in py.event.get():


            if event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:
                    posicion_inicial = list(event.pos)
                    print(posicion_inicial)



            if event.type == py.QUIT:
                print("Cerrando el juego")
                py.quit()
                quit()
        


        pantalla.fill((py.Color('black')))
        
        
        py.display.update()