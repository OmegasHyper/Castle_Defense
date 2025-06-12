from settings import *
#for testing the archer
class CollisionSprites(pg.sprite.Sprite):
    def __init__(self,pos,size,color,groups):
        super().__init__(groups)
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_frect(center =pos)