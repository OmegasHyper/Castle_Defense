import pygame as pg
from pygame import *
import json
import pytmx
from os.path import join
from os import walk
import os 
os.chdir(os.path.dirname(__file__))
import math

pg.mixer.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE= 64

### loading enemies animation ###
base_path = '../sprites/enemies/torch'
enemy_paths = {
    'N': {'walk': [], 'atk': []},
    'S': {'walk': [], 'atk': []},
    'E': {'walk': [], 'atk': []},
    'W': {'walk': [], 'atk': []}
}
strong_base_path = '../sprites/enemies/barrel'
strong_enemy_paths = {
    'N': {'walk': [], 'atk': []},
    'S': {'walk': [], 'atk': []},
    'E': {'walk': [], 'atk': []},
    'W': {'walk': [], 'atk': []}
}

# Get paths for each direction and action for enemies
for direction in enemy_paths.keys():
    for action in ['walk', 'atk']:
        folder_path = join(base_path, direction, action)
        for root_path, sub_dirs, file_names in walk(folder_path):
            if file_names:
                # Filter only PNG files and sort numerically
                png_files = [f for f in file_names if f.endswith('.png')]
                for file_name in sorted(png_files, key=lambda name: int(name.split('.')[0])):
                    full_path = join(root_path, file_name)
                    enemy_paths[direction][action].append(full_path)
                    print(f"Found path: {direction}/{action}/{file_name}")
                    
print()
## for well structured should be function
                    
for direction in strong_enemy_paths.keys():
    for action in ['walk', 'atk']:
        folder_path = join(strong_base_path, direction, action)
        for root_path, sub_dirs, file_names in walk(folder_path):
            if file_names:
                # Filter only PNG files and sort numerically
                png_files = [f for f in file_names if f.endswith('.png')]
                for file_name in sorted(png_files, key=lambda name: int(name.split('.')[0])):
                    full_path = join(root_path, file_name)
                    strong_enemy_paths[direction][action].append(full_path)
                    print(f"Found path: {direction}/{action}/{file_name}")

enemy_frames ={
        'N': { 'walk': [], 'atk': [] },
        'S': { 'walk': [], 'atk': [] },
        'E': { 'walk': [], 'atk': [] },
        'W': { 'walk': [], 'atk': [] }
    }
strong_enemy_frames ={
        'N': { 'walk': [], 'atk': [] },
        'S': { 'walk': [], 'atk': [] },
        'E': { 'walk': [], 'atk': [] },
        'W': { 'walk': [], 'atk': [] }
    }
explosion = []
Tower_upgrades = \
    {
            'level1': {
                'dmg': 100,
                'range': 600,
                'fire_rate': 50,
                'cost': 2000
            },
            'level2': {
                'dmg': 120,
                'range': 650,
                'fire_rate': 40,
                'cost' : 4000
            },
            'level3': {
                'dmg': 150,
                'range': 700,
                'fire_rate': 25,
                'cost' : 9000
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
## changed for debugging
waves = {
    '1': {
        'weak': 20,
        'strong': 10,
        'spawn_time':2000
    },
    '2': {
        'weak': 30,
        'strong': 15,
        'spawn_time':1500
    },
    '3': {
        'weak': 40,
        'strong': 20,
        'spawn_time':100
    }
}
