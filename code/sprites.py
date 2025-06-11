from settings import *

class Sprites(pg.sprite.Sprite):
    def __init__(self, groups,image, pos):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

class Ground_Sprites(pg.sprite.Sprite):
    def __init__(self,groups,image,pos):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True
