from math import acosh
from gold import *
from settings import *
from game import *
import random

attack_sound = pg.mixer.Sound("../sounds/Arrow_shot.wav")
attack_sound.set_volume(0.4)
class Arrow(pg.sprite.Sprite):
    def __init__(self, groups, archer_rect, target, state):
        super().__init__(groups)
        self.target = target
        self.front = None
        self.arrow_path = "../sprites/archers/Arrow"
        self.all_sprites = groups
        attack_sound.play()
        self.arrow_path += state + ".png"
        self.image = pg.image.load(self.arrow_path).convert_alpha()
        self.state = state
        if state == "NT":
            rect = self.image.get_frect(midbottom = archer_rect.center)
        if state == "ET":
            rect = self.image.get_frect(midleft = archer_rect.center)
        if state == "ST":
            rect = self.image.get_frect(midtop = archer_rect.center)
        if state == "WT":
            rect = self.image.get_frect(midright = archer_rect.center)
        
        self.rect = rect
        self.speed = 900
        self.damage = 100
        self.direction = pg.math.Vector2(self.target.rect.center)- pg.math.Vector2(archer_rect.center)
        self.direction = self.direction.normalize() if direction else direction
        self.archer_rect = archer_rect
        self.rotate()
    def handle_rotation(self):
        if self.state == 'ET':
            return pg.Vector2(1,0)
        if self.state == 'WT':
            return pg.Vector2(-1,0)
        if self.state == 'NT':
            return pg.Vector2(0, -1)
        if self.state == 'ST':
            return pg.Vector2(0, 1)
    def handle_angle(self,angle):
        if self.state == 'ET':
            return -angle
        if self.state == 'WT':
             return angle
        if self.state == 'NT':
            return angle
        if self.state == 'ST':
            return -angle
    def rotate(self):
        # remember: الانجل بين الاتنين الدوت على النورمين
        v1 = self.direction
        v2 = self.handle_rotation()
        dot = v2.dot(v1)
        mag_v1 = v1.magnitude()
        mag_v2 = v2.magnitude()
        cos_angle =dot/(mag_v1*mag_v2)
        angle_rad = math.acos(cos_angle)
        angle_deg = math.degrees(angle_rad)
        rotate_image= pg.transform.rotate(self.image,self.handle_angle(angle_deg))
        self.image = rotate_image

    def update(self, dt):
        self.rect.center += self.speed * self.direction * dt
        
        if self.target.rect.contains(self.rect):
            self.target.health -= self.damage
            #print(self.target.health)

            # if self.target.health <= 0:           ## not safe to be used as kill should work from enemy update method
            #     self.target.get_killed()

            if self.target.health <= 0:
                
                quantity = random.randint(20, 50)
                gold(self.all_sprites, quantity, self.target.rect.center)

            self.kill()
