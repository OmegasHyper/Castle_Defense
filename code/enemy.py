from settings import *
from Queue import Queue
#from ground import collisionsprites

BLACK = (0, 0, 0)
RED = (220, 20, 60)
DARK_RED = (139, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
die_sound = pg.mixer.Sound("../sounds/goblin_death.wav")
die_sound.set_volume(0.4)
goblin_attack_sound = pg.mixer.Sound("../sounds/goblin_attack.wav")
goblin_attack_sound.set_volume(0.3)
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
        self.healthbar_offset_x = 0
        self.healthbar_offset_y = 45
        self.max_health = 500
        self.strong = strong 
        if strong :
            self.image = Enemy.Strongimage 
            self.damage = 20
            self.health = self.max_health = 200
            self.healthbar_offset_x = -40
            self.healthbar_offset_y = +15
            print("strong created")
        else: 
            print("weak created")     ## debugging
            self.damage = 1

        ## HEALTH PRE-RENDERING (OPTIMIZE FPS) AND INITIALIZATION
        self.health_bar_width = 60
        self.health_bar_height = 8
        self.health_bar_bg = pg.Surface((self.health_bar_width, self.health_bar_height), pg.SRCALPHA)
        pg.draw.rect(self.health_bar_bg, (0, 0, 0), (0, 0, self.health_bar_width, self.health_bar_height),
                     border_radius=4)



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

    def load_health_bar(self, offset):
        x = self.rect.centerx - self.health_bar_width // 2 + offset.x +  self.healthbar_offset_x
        y = self.rect.top +  self.healthbar_offset_y + offset.y

        self.display.blit(self.health_bar_bg, (x, y))

        health_ratio = max(self.health, 0) / self.max_health
        if health_ratio > 0:
            health_width = int((self.health_bar_width - 4) * health_ratio)
            health_rect = pg.Rect(x + 2, y + 2, health_width, self.health_bar_height - 4)
            pg.draw.rect(self.display, (220, 20, 60), health_rect, border_radius=3)

    def collision(self , direction):
        for spr in self.collision_spr:
            for sprite in spr:
                if self.rect.colliderect(sprite.hitbox):
                    if(direction == 'x'):
                        if self.direction.x > 0 : self.hitbox_rect.right = sprite.hitbox.left
                        if self.direction.x < 0: self.hitbox_rect.left = sprite.hitbox.right
                    else:
                        if self.direction.y > 0: self.hitbox_rect.bottom = sprite.hitbox.top
                        if self.direction.y < 0 : self.hitbox_rect.top = sprite.hitbox.bottom
                    self.rect.center = self.hitbox_rect.center
                    if self.isAttacking:
                        goblin_attack_sound.play()
                        now = pg.time.get_ticks()
                        if now - self.last_attack > self.atk_speed:
                            self.last_attack =now
                            sprite.health -=self.damage
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
        self.load_health_bar(x)
        if self.ismoving:
            self.display.blit(self.image,self.rect.topleft + x)



    def update(self,dt):
        if self.ismoving :
            self.collision(self.direction)
            self.move(dt)
            self.animate(dt)



    def get_killed(self):
        Enemy.number_eneimes -= 1
        die_sound.play()
        self.kill()
        


