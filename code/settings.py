import pygame as pg
from pygame import *
import json
import pytmx
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
Tower_upgrades = \
    {
            'level1': {
                'dmg': 10,
                'range': 120,
                'fire_rate': 10
            },
            'level2': {
                'dmg': 40,
                'range': 200,
                'fire_rate': 20
            },
            'level3': {
                'dmg': 120,
                'range': 350,
                'fire_rate': 30
            }
        }
Player_upgrades =\
    {
'level1':{
    'dmg': 30 ,
    'atk_speed':30,
    'speed': 30
},
'level2':{
    'dmg': 60 ,
    'atk_speed':60,
    'speed': 60
},
'level3':{
    'dmg': 90 ,
    'atk_speed':90,
    'speed': 90
},
}
menu_background = pg.image.load('../sprites/menu_background.jpg')
menu_background_rect = menu_background.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))



