from settings import *

class Collision_sprites(pg.sprite.Sprite):
    def __init__(self, groups,image, pos):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)