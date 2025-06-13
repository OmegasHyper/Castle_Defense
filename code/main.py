from settings import *
import pygame as pg
from game import *
from main_menu import *
import os 
os.chdir(os.path.dirname(__file__))
main_menu_sound = pg.mixer.Sound("../sounds/main_menu.mp3")
ingame_sound = pg.mixer.Sound("../sounds/ingame.mp3")
ingame_sound.set_volume(0.2)

# palmer , bellingham , saka , toney , trent ---> pressure!!! _______  what pressure?
class Game_Mannager:
    def __init__(self):
        self.running = True
        pg.init()
        self.display = pg.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pg.display.set_caption('Castle Defense')
        self.main_menu = Main_Menu(self.display,self)
        self.game =  Game(self.display , self)
        self.clock = pg.time.Clock()
        self.state = 'menu'
        self.load()
        self.state_switched = False
        main_menu_sound.play(loops=-1)
        
    def load(self):
        for direction in enemy_paths.keys():
            for action in ['walk', 'atk']:
                for full_path in enemy_paths[direction][action]:
                        surf = pg.image.load(full_path).convert_alpha()
                        enemy_frames[direction][action].append(surf)

        for direction in strong_enemy_paths.keys():
            for action in ['walk', 'atk']:
                for full_path in strong_enemy_paths[direction][action]:
                        surf = pg.image.load(full_path).convert_alpha()
                        strong_enemy_frames[direction][action].append(surf)
                        
    def run(self):
        while self.running:
            dt = self.clock.tick_busy_loop(60)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.running = False

            if self.state == 'menu':
                self.main_menu.draw()

            elif self.state == 'game':
                self.game.update(dt)
                if not  self.state_switched  :
                    main_menu_sound.stop()
                    ingame_sound.play(loops=-1)
                    self.state_switched = True
                # self.game.draw()

            pg.display.update()
    pg.quit()

if __name__ == '__main__':
    game_manager = Game_Mannager()
    game_manager.run()