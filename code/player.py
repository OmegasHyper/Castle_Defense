from settings import *
from ground import collisionsprites

class Player(pg.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pg.image.load("../sprites/player/walk/tile000.png")
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.speed = 100
        self.direction = pg.Vector2()

    def input(self):
        keys = pg.key.get_pressed()
        self.direction.x = int(keys[pg.K_d]) - int(keys[pg.K_a])
        self.direction.y = int(keys[pg.K_s]) - int(keys[pg.K_w])
    def update(self,dt):
        self.input()
        self.rect.center += self.direction *self.speed * dt

    def animate(self):
        pass
