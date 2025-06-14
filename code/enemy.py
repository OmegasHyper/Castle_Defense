from Castle_Defense.code.allsprites import AllSprites
from settings import *
from Queue import Queue
from gold import *
from random import randint
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
    show_hitboxes = True

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
        self.all_sprites = groups[0]
        Enemy.number_eneimes +=1
        Enemy.total_eneimes+=1
        self.display = pg.display.get_surface()
        
        self.state = state
        self.action = walk
        self.frame_index = 0
        self.collision_spr = collision_spr
        self.hitbox_rect = self.rect.copy().inflate(-80,-80)
        self.atk_speed = 1000     #for timer
        self.isAttacking = False #for timer
        self.last_attack = 0    #for timer
        self.healthbar_offset_x = 0
        self.healthbar_offset_y = 45
        self.max_health = 500
        self.strong = strong 
        self.obst = True
        self.piriority = "low"

        if strong :
            self.image = Enemy.Strongimage
            self.speed = 150
            self.damage = 20
            self.health = self.max_health = 200
            self.healthbar_offset_x = -40
            self.healthbar_offset_y = +15
            self.piriority = "high"
            self.hitbox_offset_x = -35
            self.hitbox_offset_y = -20
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
        self.isAttacking = False
        for spr in self.collision_spr:
            for sprite in spr:
                if self.hitbox_rect.colliderect(sprite.hitbox):
                    self.isAttacking = True
                    if(direction == 'x'):
                        if self.direction.x > 0 : self.hitbox_rect.right = sprite.hitbox.left
                        if self.direction.x < 0: self.hitbox_rect.left = sprite.hitbox.right
                    else:
                        if self.direction.y > 0: self.hitbox_rect.bottom = sprite.hitbox.top
                        if self.direction.y < 0 : self.hitbox_rect.top = sprite.hitbox.bottom
                    if self.strong:
                        self.rect.centerx = self.hitbox_rect.centerx - self.hitbox_offset_x
                        self.rect.centery = self.hitbox_rect.centery - self.hitbox_offset_y
                    if self.isAttacking:
                        #if(hasattr(sprite , 'obst')) and self.obst : self.health-=80 ; self.obst = False;
                        now = pg.time.get_ticks()
                        if now - self.last_attack > self.atk_speed:
                            goblin_attack_sound.play()
                            self.last_attack =now
                            if(hasattr(sprite , 'obst')) :sprite.obst_health_dec(self.damage)
                            else: sprite.health -=self.damage

                
        if not self.isAttacking:
            self.obst = True
    
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
        if self.strong:
            self.rect.centerx = self.hitbox_rect.centerx - self.hitbox_offset_x
            self.rect.centery = self.hitbox_rect.centery - self.hitbox_offset_y


    """" def draw_hitbox(self, offset):
        #Draw the hitbox rectangle for debugging
        if Enemy.show_hitboxes:
            # Calculate hitbox position with offset
            hitbox_pos = (self.hitbox_rect.x + offset.x, self.hitbox_rect.y + offset.y)
            hitbox_rect = pg.Rect(hitbox_pos, self.hitbox_rect.size)

            # Choose color based on enemy type and state
            if self.strong:
                color = 'blue' if not self.isAttacking else 'red'
            else:
                color = 'blue' if not self.isAttacking else 'red'

            # Draw hitbox outline
            pg.draw.rect(self.display, color, hitbox_rect, 2)

            # Optional: Draw center point
            center_pos = (hitbox_rect.centerx, hitbox_rect.centery)
            pg.draw.circle(self.display, color, center_pos, 3) """
    def draw( self,x):
        self.load_health_bar(x)
        if self.ismoving:
            self.display.blit(self.image,self.rect.topleft + x)


    def update(self,dt):
        if self.ismoving :
            self.collision(self.direction)
            self.move(dt)
            self.animate(dt)
        if self.health <= 0:           
            self.get_killed()



    def get_killed(self):
        Enemy.number_eneimes -= 1
        quantity = randint(20, 50)
        gold(self.all_sprites, quantity, self.rect.center)
        die_sound.play()
        self.kill()
        


