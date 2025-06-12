from settings import *
from game import *
class Arrow(pg.sprite.Sprite):
    def __init__(self, direction, archer_rect, target, groups):
        super().__init__(groups)
        self.target = target
        self.front = None
        self.arrow_path = "../sprites/archers/Arrow"
        self.arrow_path += direction + ".png"
        self.image = pg.image.load(self.arrow_path).convert_alpha()
        if direction == "NT":
            rect = self.image.get_frect(midbottom = archer_rect.midtop)
        if direction == "ET":
            rect = self.image.get_frect(midleft = archer_rect.midright)
        if direction == "ST":
            rect = self.image.get_frect(midtop = archer_rect.midbottom)
        if direction == "WT":
            rect = self.image.get_frect(midright = archer_rect.midleft)
        
        self.rect = rect
        self.speed = 300
        self.direction = pg.math.Vector2(self.target.rect.center)- pg.math.Vector2(archer_rect.center)
        self.direction = self.direction.normalize() if direction else direction
        #self.velocity = direction.normalize() * self.speed

    def update(self, dt):
        self.rect.center += self.speed * self.direction * dt
        #if pg.sprite.spritecollide(self, )
        if self.rect.centerx >= 4600:
            self.kill()
