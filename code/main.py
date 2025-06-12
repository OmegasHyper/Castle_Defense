from settings import *
import pygame as pg
from game import *
from main_menu import *
import os 
os.chdir(os.path.dirname(__file__))

#a7la mesa 3la billy
# palmer , bellingham , saka , toney , trent ---> pressure!!! _______  what pressure?
class Game_Mannager:
    def __init__(self):
        self.running = True
        pg.init()
        self.display = pg.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pg.display.set_caption('Castle Defense')
        self.main_menu = Main_Menu(self.display,self)
        self.game = Game(self.display , self)
        self.clock = pg.time.Clock()
        self.state = 'menu'

    def run(self):
        while self.running:
            dt = self.clock.tick_busy_loop(60)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            if self.state == 'menu':
                self.main_menu.draw()
            elif self.state == 'game':
                self.game.update(dt)
                self.game.draw()

            pg.display.update()
    pg.quit()

if __name__ == '__main__':
    game_manager = Game_Mannager()
    game_manager.run()