# --- Imports ---
import pygame.mixer as mixer

music_configs = {
    'actual_music_path': ''
}


def set_music_path(music_path: str):
    music_configs['actual_music_path'] = music_path

def play_music():
    """
    Verifica que el path no esté vacío, de no ser así, le da play a la musica
    """
    if music_configs.get('actual_music_path'):
        mixer.music.load(music_configs.get('actual_music_path'))
        #mixer.music.set_volume(0.3)   -> Lo autosetea, no nos sirve D=
        mixer.music.play(-1, 0, 2500) #Loop, empieza del 0, fade time
        


def get_actual_volume() -> int:
    actual_vol = mixer.music.get_volume() * 100
    return round(actual_vol, 0)

def set_volume(volume: int):
    actual_vol = volume / 100
    actual_vol = round(actual_vol, 1)
    mixer.music.set_volume(actual_vol)

def stop_music():
    if music_configs.get('actual_music_path') and mixer.music.get_busy():
        mixer.music.fadeout(500)