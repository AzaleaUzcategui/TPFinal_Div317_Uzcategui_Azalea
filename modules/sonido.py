# --- Imports ---
import pygame.mixer as mixer

music_configs = {
    'actual_music_path': '',
    'click_sound': None,
    'click_volume': 0.5
}


def inicializar_mixer():
    if not mixer.get_init():
        mixer.init()


def set_music_path(music_path: str):
    music_configs['actual_music_path'] = music_path


def play_music():
    """
    Verifica que el path no este vacio; si hay ruta, reproduce en loop.
    """
    if music_configs.get('actual_music_path'):
        inicializar_mixer()
        mixer.music.load(music_configs.get('actual_music_path'))
        mixer.music.play(-1, 0, 2500)


# LE volume
def get_actual_volume() -> int:
    actual_vol = mixer.music.get_volume() * 100
    return round(actual_vol, 0)


def set_volume(volume: int):
    actual_vol = volume / 100
    actual_vol = round(actual_vol, 1)
    mixer.music.set_volume(actual_vol)



def stop_music():
    """
    Para la musica con fadeout :)
    """
    if music_configs.get('actual_music_path') and mixer.music.get_busy():
        mixer.music.fadeout(500)


def load_click(path: str):
    """
    Carga sonido de click
    """
    inicializar_mixer()
    music_configs['click_sound'] = mixer.Sound(path)
    music_configs['click_sound'].set_volume(music_configs.get('click_volume', 0.5))


def play_click():
    """
    Plays the soudn
    """
    if music_configs.get('click_sound'):
        inicializar_mixer()
        music_configs['click_sound'].play()


def set_click_volume(volume: int):
    """
    Setea el volumen
    """
    volume = max(0, min(100, volume))
    music_configs['click_volume'] = volume / 100
    if music_configs.get('click_sound'):
        music_configs['click_sound'].set_volume(music_configs['click_volume'])


def cargar_sonido(path: str, volume_pct: int = 100):
    """
    Carga y devuelve un Sound con el volumen seteado (0-100).
    """
    inicializar_mixer()
    snd = mixer.Sound(path)
    snd.set_volume(max(0, min(100, volume_pct)) / 100)
    return snd
