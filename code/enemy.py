from settings import *
from Queue import Queue
#from ground import collisionsprites


class Enemy(pg.sprite.Sprite):
    image = pg.image.load("../sprites/enemies/torch/E/walk/3.png")
    Strongimage = pg.image.load("../sprites/enemies/barrel/N/walk/1.png")
    spawn =True
    number_eneimes = 0
    total_eneimes = 0
    spawn_time = 0
    last_spawn_t = pg.time.get_ticks()

    def __init__(self,groups,pos,state, collision_spr, strong):
        super().__init__(groups)
        self.animate_speed = 24
        self.health = 500
        self.image= Enemy.image
        self.rect = self.image.get_frect(center=pos)
        self.speed = 200
        self.direction = pg.Vector2(0, -1)
        self.ismoving = False
        self.enemy = True
        Enemy.number_eneimes +=1
        Enemy.total_eneimes+=1
        self.display = pg.display.get_surface()
        print(Enemy.number_eneimes)
        self.state = state
        self.action = walk
        self.frame_index = 0
        self.collision_spr = collision_spr
        self.hitbox_rect = self.rect
        self.atk_speed = 500     #for timer
        self.isAttacking = True #for timer
        self.last_attack = 0    #for timer
        self.strong = strong 
        if strong :self.image = Enemy.Strongimage 
        

        ## will be changed  (debugging )
    def direction_func (self,x = 0 , y=-1 ):
        # takes the direction as x and y make vector and normalize
        # x -> 0-1   y -> 0-1 
        self.direction = pg.Vector2(x,y)
        self.direction = self.direction.normalize() if self.direction else self.direction
    @staticmethod
    def spawning():
        recent_spawn =pg.time.get_ticks() 
        if recent_spawn - Enemy.last_spawn_t > Enemy.spawn_time:
            Enemy.spawn = True
            Enemy.last_spawn_t = recent_spawn
        else : Enemy.spawn = False
    def collision(self , direction):
        for sprite in self.collision_spr:
            if self.rect.colliderect(sprite.hitbox):
                if(direction == 'x'):
                    if self.direction.x > 0 : self.hitbox_rect.right = sprite.hitbox.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.hitbox.right
                else:
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.hitbox.top
                    if self.direction.y < 0 : self.hitbox_rect.top = sprite.hitbox.bottom
                self.rect.center = self.hitbox_rect.center
                if self.isAttacking:
                    now = pg.time.get_ticks()
                    if now - self.last_attack > self.atk_speed:
                        self.last_attack =now
                        sprite.health -=1
                else:
                    self.isAttacking = False

    def handle_direction(self):
        if self.state == 'N':
            self.direction_func(0,1)
        if self.state == 'W':
            self.direction_func(1, 0)
        if self.state == 'E':
            self.direction_func(-1, 0)
        if self.state == 'S':
            self.direction_func(0, -1)

    def animate(self,dt):
        if self.ismoving:
            if self.strong:
                self.frame_index = self.frame_index + self.animate_speed * dt if self.direction else 0
                self.image = strong_enemy_frames[self.state]['walk'][int(self.frame_index) % len(strong_enemy_frames[self.state]['walk'])]
            else : 
                self.frame_index = self.frame_index + self.animate_speed * dt if self.direction else 0
                self.image = enemy_frames[self.state]['walk'][int(self.frame_index) % len(enemy_frames[self.state]['walk'])]
    def move(self,dt):
        self.handle_direction()
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('x')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('y')
        self.rect.center = self.hitbox_rect.center
    def draw( self,x):
        if self.ismoving:
            self.display.blit(self.image,self.rect.topleft + x)

    def update(self,dt):
        if self.ismoving :
            self.collision(self.direction)
            self.move(dt)
            self.animate(dt)

    def get_killed(self):
        Enemy.number_eneimes -= 1
        self.kill()
        


