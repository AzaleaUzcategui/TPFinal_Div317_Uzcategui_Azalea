# --- Imports ---
import pygame as py


# ----- Configuraciones fijas del juego ---------
DIMENSION_PANTALLA = (1000, 700)
TITULO = "Dragon Ball Z || Trading Card Game [TCG]"
FPS = 30


# ------- Datos de jugador --------
CANTIDAD_DE_VIDAS = 3
VOLUMEN_INICIAL = 50


# -------- Imágenes --------
ICONO_SURFACE = py.image.load("assets/img/icons/1_star.png")


# ------- FONT -----
FUENTE_ALAGARD = "assets/fonts/alagard.ttf"


# ---- Diccionario de formularios -----
dict_forms_status = {}


# --- File ranking ----
RANKING_CSV = 'modules/puntajes.csv'

# ----------- imagenes ---------
FONDO_MENU = 'assets/img/forms/form_main_menu.png'
FONDO_RANKING = 'assets/img/forms/form_ranking.png'
FONDO_OPCIONES = 'assets/img/forms/form_options.png'



# -------- Musica --------
MUSICA_RANKING = 'assets/audio/music/form_ranking.ogg'
MUSICA_MENU = 'assets/audio/music/menu_music.ogg'
MUSICA_OPCIONES = 'assets/audio/music/form_options.ogg'