from settings import *
from player import *
class Game:
    def __init__(self,display , gamemanager):
        self.display = display
        self.gamemanager = gamemanager
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self.all_sprites)

    def update(self,dt):
        self.player.update(dt)
    def draw (self):
        self.display.fill('blue')
        self.all_sprites.draw(self.display)