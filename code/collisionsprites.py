from settings import *
#for testing the archer
class CollisionSprites(pg.sprite.Sprite):
    def __init__(self,pos,size,groups):
        super().__init__(groups)
        self.image = pg.Surface(size)
        self.image.fill('red')
        self.rect = self.image.get_frect(center =pos)