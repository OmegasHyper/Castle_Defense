from settings import *

class Collision_sprites(pg.sprite.Group):
    def __init__(self, pos, surf,groups):

        self.image = surf
        self.rect = self.image.get_rect(center=pos)