from settings import *

class Arrow(pg.sprite.Sprite):
    def __init__(self,pos,target_pos,groups):
        super().__init__(groups)
        self.image = pg.image.load('arrow.jpg').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = 10
        direction = pg.math.Vector2(target_pos)- pg.math.Vector2(pos)
        self.velocity = direction.normalize() * self.speed

    def update(self):
        self.rect.center += self.velocity.x
        self.rect.centery -= self.velocity.y