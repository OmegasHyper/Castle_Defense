from settings import *

class Game:
    def __init__(self,display , gamemanager):
        self.display = display
        self.gamemanager = gamemanager
    def update(self,dt):
        pass
    def draw (self):
        self.display.fill('blue')