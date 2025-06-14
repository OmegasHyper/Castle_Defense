import pygame as pg 
class Obstacles(pg.sprite.Sprite) :
    image = pg.image.load("../sprites/Obstacles/obstacle.png")
    imsc = pg.transform.smoothscale_by(image,(0.3,0.3))
    def __init__(self,groups,pos):
        super().__init__(groups)
        self.image = Obstacles.imsc
        self.rect = self.image.get_frect(center=pos)
        self.health = 100
        self.hitbox = self.rect.inflate(-140,-180)
        self.hitbox.top += 10
        
    

    