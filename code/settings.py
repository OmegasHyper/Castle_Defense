import pygame as pg
from pygame import *
import json
import pytmx
from os.path import join
from os import walk
import os 
os.chdir(os.path.dirname(__file__))
import math

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
## changed for debugging
waves = {
    '1': {
        'weak': 1,
        'strong': 2,
        'spawn_time':2000
    },
    '2': {
        'weak': 0,
        'strong': 4,
        'spawn_time':1000
    },
    '3': {
        'weak': 50,
        'strong': 15,
        'spawn_time':800
    }
}
