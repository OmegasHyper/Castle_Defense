from settings import *
from Queue import Queue
#from ground import collisionsprites

class Enemy(pg.sprite.Sprite):
    image = pg.image.load("../sprites/enemies/torch/E/walk/3.png")
    spawn =True
    number_eneimes = 0
    spawn_time = 2000
    last_spawn_t = pg.time.get_ticks()
    

    def __init__(self,groups,pos):
        super().__init__(groups)
        self.image= Enemy.image
        self.rect = self.image.get_frect(center=pos)
        self.speed = 200
        self.direction = pg.Vector2(0, -1)
        self.ismoving = False
        self.enemy = True
        Enemy.number_eneimes +=1
        self.display = pg.display.get_surface()
        print(Enemy.number_eneimes)
        
        ## will be changed  (debugging )
    def direction_func (self,x = 0 , y=-1 ):
        # takes the direction as x and y make vector and normalize
        # x -> 0-1   y -> 0-1 
        self.direction = pg.Vector2(x,y)
        self.direction = self.direction.normalize() if self.direction else self.direction
    def spawning():
        recent_spawn =pg.time.get_ticks() 
        if recent_spawn - Enemy.last_spawn_t > Enemy.spawn_time:
            Enemy.spawn = True
            Enemy.last_spawn_t = recent_spawn
        else : Enemy.spawn = False


    def move(self,dt):
        self.rect.center += self.speed*self.direction*dt
    def draw( self,x):
        if self.ismoving:
            self.display.blit(self.image,self.rect.topleft + x)

    def update(self,dt):
        if self.ismoving :
            self.move(dt)
        


