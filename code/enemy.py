from settings import *
from Queue import Queue
#from ground import collisionsprites


class Enemy(pg.sprite.Sprite):
    image = pg.image.load("../sprites/enemies/torch/E/walk/3.png")
    spawn =True
    number_eneimes = 0
    spawn_time = 2000
    last_spawn_t = pg.time.get_ticks()

    def __init__(self,groups,pos,state):
        super().__init__(groups)
        self.animate_speed = 24
        self.image= Enemy.image
        self.rect = self.image.get_frect(center=pos)
        self.speed = 200
        self.direction = pg.Vector2(0, -1)
        self.ismoving = False
        self.enemy = True
        Enemy.number_eneimes +=1
        self.display = pg.display.get_surface()
        print(Enemy.number_eneimes)
        self.state = state
        self.action = walk
        self.frame_index = 0
        self.frames ={
        'N': { 'walk': [], 'atk': [] },
        'S': { 'walk': [], 'atk': [] },
        'E': { 'walk': [], 'atk': [] },
        'W': { 'walk': [], 'atk': [] }
    }
        self.load()

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
            self.frame_index = self.frame_index + self.animate_speed * dt if self.direction else 0
            self.image = self.frames[self.state]['walk'][int(self.frame_index) % len(self.frames[self.state]['walk'])]


    def load(self):
        for direction in enemy_paths.keys():
            for action in ['walk', 'atk']:
                for full_path in enemy_paths[direction][action]:
                    try:
                        surf = pg.image.load(full_path).convert_alpha()
                        self.frames[direction][action].append(surf)
                        print(f"Loaded image: {full_path}")
                    except enemy_paths.error as e:
                        print(f"Error loading {full_path}: {e}")

        print(self.frames)

    def move(self,dt):
        self.handle_direction()
        self.rect.center += self.speed*self.direction*dt
    def draw( self,x):
        if self.ismoving:
            self.display.blit(self.image,self.rect.topleft + x)

    def update(self,dt):
        if self.ismoving :
            self.move(dt)
            self.animate(dt)
        


