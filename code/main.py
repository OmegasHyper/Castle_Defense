from settings import *
import pygame as pg
from game import *
from main_menu import *
from pause_menu import *
import os
os.chdir(os.path.dirname(__file__))

#a7la mesa 3la billy
# palmer , bellingham , saka , toney , trent ---> pressure!!! _______  what pressure?
class Game_Mannager:
    def __init__(self):
        self.running = True
        self.paused = False
        pg.init()
        self.display = pg.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pg.display.set_caption('Castle Defense')
        self.main_menu = Main_Menu(self.display,self)
        self.game =  Game(self.display , self)
        self.clock = pg.time.Clock()
        self.state = 'menu'
        self.load()

    def load(self):
        for direction in enemy_paths.keys():
            for action in ['walk', 'atk']:
                for full_path in enemy_paths[direction][action]:
                        surf = pg.image.load(full_path).convert_alpha()
                        enemy_frames[direction][action].append(surf)
                        
    def run(self):
        while self.running:
            dt = self.clock.tick_busy_loop(60)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.running = False

            if self.paused and self.state =='pause':
                self.pause_menu.update()
            elif self.state == 'menu':
                self.main_menu.draw()
            elif self.state == 'game':
                self.game.update(dt)
                self.pause_menu = Pause_menu(self.display, self)

                # self.game.draw()        
            elif self.state == 'pause':
                self.paused = not self.paused
                for i in range(20):
                    self.pause_menu = Pause_menu(self.display, self)
                #self.pause_menu.display_copy = self.display.copy()
            elif self.state == 'shop':
                pass
            pg.display.update()
    pg.quit()

if __name__ == '__main__':
    game_manager = Game_Mannager()
    game_manager.run()