# ---- Imports ----
import pygame as py
import modules.forms.form_base as base_form
from utn_fra.pygame_widgets import (Label, Button)
import modules.variables as var

def create_stage_form(dict_form_data: dict) -> dict:
    form = base_form.create_base_form(dict_form_data)

    form['stage_restart'] = False
    form['time_finished'] = False #Flag
    form['actual_level'] = 1
    form['stage_timer'] = var.STAGE_TIMER

    #Bonuses
    form['bonus_shield_avaliable'] = True
    form['bonus_heal_avaliable'] = True

    form['bonus_shield_applied'] = False

    form['stage'] = None #Crear modulo para stage

    form['clock'] = py.time.Clock()

    
 