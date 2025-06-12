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
            rect = self.image.get_frect(midbottom = archer_rect.center)
        if direction == "ET":
            rect = self.image.get_frect(midleft = archer_rect.center)
        if direction == "ST":
            rect = self.image.get_frect(midtop = archer_rect.center)
        if direction == "WT":
            rect = self.image.get_frect(midright = archer_rect.center)
        
        self.rect = rect
        self.speed = 300
        self.damage = 100
        self.direction = pg.math.Vector2(self.target.rect.center)- pg.math.Vector2(archer_rect.center)
        self.direction = self.direction.normalize() if direction else direction

    def update(self, dt):
        self.rect.center += self.speed * self.direction * dt
        
        if self.target.rect.contains(self.rect):
            self.target.health -= self.damage
            #print(self.target.health)
            if self.target.health <= 0:
                self.target.get_killed()
            self.kill()
