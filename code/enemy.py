from settings import *
from Queue import Queue
from gold import *
from random import randint
import allsprites

# from ground import collisionsprites

BLACK = (0, 0, 0)
RED = (220, 20, 60)
DARK_RED = (139, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
die_sound = pg.mixer.Sound("../sounds/goblin_death.wav")
die_sound.set_volume(0.1)
goblin_attack_sound = pg.mixer.Sound("../sounds/goblin_attack.wav")
goblin_attack_sound.set_volume(0.1)


class Enemy(pg.sprite.Sprite):
    image = pg.image.load("../sprites/enemies/torch/E/walk/3.png")
    Strongimage = pg.image.load("../sprites/enemies/barrel/N/walk/1.png")
    spawn = True
    number_eneimes = 0
    total_eneimes = 0
    spawn_time = 0

    last_spawn_t = pg.time.get_ticks()
    show_hitboxes = True

    def __init__(self,groups,pos,state, collision_spr, strong, round):

        super().__init__(groups)
        self.round = round
        # print(self.round) #for debugging
        # Enemy.live_enemies +=1
        self.animate_speed = 24
        self.health = 500
        self.image = Enemy.image
        self.rect = self.image.get_frect(center=pos)
        self.speed = 200
        self.direction = pg.Vector2(0, -1)
        self.ismoving = False
        self.enemy = True
        self.all_sprites = groups[0]
        Enemy.number_eneimes += 1
        Enemy.total_eneimes += 1
        self.display = pg.display.get_surface()

        self.state = state
        self.action = walk
        self.frame_index = 0
        self.collision_spr = collision_spr
        self.hitbox_rect = self.rect.copy().inflate(-80, -80)
        self.atk_speed = 1000  # for timer
        self.att_animation_speed = 10
        self.isAttacking = False  # for timer
        self.last_attack = 0  # for timer
        self.healthbar_offset_x = 0
        self.healthbar_offset_y = 45
        self.max_health = 500
        self.strong = strong
        self.obst = True
        self.piriority = "low"

        if strong:
            self.image = Enemy.Strongimage
            self.speed = 150
            self.damage = 30
            self.health = self.max_health = 200
            self.healthbar_offset_x = -40
            self.healthbar_offset_y = +15
            self.piriority = "high"
            self.hitbox_offset_x = -35
            self.hitbox_offset_y = -20
            # Explosion-related variables for strong enemies only
            self.explosion_frame_index = 0
            self.explosion_animation_speed = 20
            self.last_explosion_frame = 0
            self.explosion_cooldown = 100
            self.isExploding = False
            self.explosion_triggered = False
            # print("strong created")

        else:
            # print("weak created")  ## debugging
            self.damage = 2

        ## HEALTH PRE-RENDERING (OPTIMIZE FPS) AND INITIALIZATION
        self.health_bar_width = 60
        self.health_bar_height = 8
        self.health_bar_bg = pg.Surface((self.health_bar_width, self.health_bar_height), pg.SRCALPHA)
        pg.draw.rect(self.health_bar_bg, (0, 0, 0), (0, 0, self.health_bar_width, self.health_bar_height),
                     border_radius=4)

    def direction_func(self, x=0, y=-1):
        # takes the direction as x and y make vector and normalize
        # x -> 0-1   y -> 0-1
        self.direction = pg.Vector2(x, y)
        self.direction = self.direction.normalize() if self.direction else self.direction

    @staticmethod
    def spawning():
        recent_spawn = pg.time.get_ticks()
        if recent_spawn - Enemy.last_spawn_t > Enemy.spawn_time:
            Enemy.spawn = True
            Enemy.last_spawn_t = recent_spawn
        else:
            Enemy.spawn = False

    def load_health_bar(self, offset):
        x = self.rect.centerx - self.health_bar_width // 2 + offset.x + self.healthbar_offset_x
        y = self.rect.top + self.healthbar_offset_y + offset.y

        self.display.blit(self.health_bar_bg, (x, y))

        health_ratio = max(self.health, 0) / self.max_health
        if health_ratio > 0:
            health_width = int((self.health_bar_width - 4) * health_ratio)
            health_rect = pg.Rect(x + 2, y + 2, health_width, self.health_bar_height - 4)
            pg.draw.rect(self.display, (220, 20, 60), health_rect, border_radius=3)

    def collision(self, direction, dt):
        for spr in self.collision_spr:
            for sprite in spr:
                if self.hitbox_rect.colliderect(sprite.hitbox):
                    self.isAttacking = True
                    if (direction == 'x'):
                        if self.direction.x > 0: self.hitbox_rect.right = sprite.hitbox.left
                        if self.direction.x < 0: self.hitbox_rect.left = sprite.hitbox.right
                    else:
                        if self.direction.y > 0: self.hitbox_rect.bottom = sprite.hitbox.top
                        if self.direction.y < 0: self.hitbox_rect.top = sprite.hitbox.bottom
                    if self.strong:
                        self.rect.centerx = self.hitbox_rect.centerx - self.hitbox_offset_x
                        self.rect.centery = self.hitbox_rect.centery - self.hitbox_offset_y

                    if self.isAttacking and (not self.strong or not self.isExploding):
                        now = pg.time.get_ticks()
                        if now - self.last_attack > self.atk_speed:
                            goblin_attack_sound.play()
                            self.last_attack = now
                            # Deal damage to obstacles and other sprites
                            if hasattr(sprite, 'isObstacle'):
                                sprite.obst_health_dec(self.damage)
                            else:
                                sprite.health -= self.damage

        if not self.isAttacking:
            self.obst = True

    def handle_direction(self):
        if self.state == 'N':
            self.direction_func(0, 1)
        if self.state == 'W':
            self.direction_func(1, 0)
        if self.state == 'E':
            self.direction_func(-1, 0)
        if self.state == 'S':
            self.direction_func(0, -1)

    def should_start_explosion(self):
        if self.strong and self.isAttacking and not self.explosion_triggered:
            # Check if we've reached frame index 2 in the attack animation
            current_frame = int(self.frame_index) % len(strong_enemy_frames[self.state]['atk'])
            if current_frame == 2:
                return True
        return False

    def explosion_animation(self, dt):
        self.explosion_frame_index += self.explosion_animation_speed * dt
        current_explosion_frame = int(self.explosion_frame_index) % len(explosion)
        self.image = explosion[current_explosion_frame]

        # Center the explosion sprite properly
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)

        # Check if explosion animation is complete
        if self.explosion_frame_index >= len(explosion):
            self.deal_explosion_damage()
            self.get_killed()

    def deal_explosion_damage(self):
        for spr in self.collision_spr:
            for sprite in spr:
                if self.hitbox_rect.colliderect(sprite.hitbox):
                    if hasattr(sprite, 'isObstacle'):
                        sprite.obst_health_dec(self.damage)
                    else:
                        sprite.health -= self.damage

    def animate(self, dt):
        if self.strong and self.isExploding:
            self.explosion_animation(dt)
        elif self.isAttacking:
            self.frame_index += self.att_animation_speed * dt

            if self.strong:
                # Check if we should start explosion
                if self.should_start_explosion():
                    self.isExploding = True
                    self.explosion_triggered = True
                    self.explosion_frame_index = 0
                    return

                # Continue attack animation
                self.image = strong_enemy_frames[self.state]['atk'][
                    int(self.frame_index) % len(strong_enemy_frames[self.state]['atk'])]
            else:
                self.image = enemy_frames[self.state]['atk'][
                    int(self.frame_index) % len(enemy_frames[self.state]['atk'])]
        elif self.ismoving:
            self.frame_index += self.animate_speed * dt
            if self.strong:
                self.image = strong_enemy_frames[self.state]['walk'][
                    int(self.frame_index) % len(strong_enemy_frames[self.state]['walk'])]
            else:
                self.image = enemy_frames[self.state]['walk'][
                    int(self.frame_index) % len(enemy_frames[self.state]['walk'])]

    def move(self, dt):
        if self.strong and self.isExploding:
            return  # Don't move while exploding

        self.handle_direction()
        self.isAttacking = False  # this line is important for the atk animations to work in all states (NSEW)
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('y', dt)
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('x', dt)
        self.rect.center = self.hitbox_rect.center
        if self.strong:
            self.rect.centerx = self.hitbox_rect.centerx - self.hitbox_offset_x
            self.rect.centery = self.hitbox_rect.centery - self.hitbox_offset_y

    def draw(self, x):
        self.load_health_bar(x)
        if self.ismoving or (self.strong and self.isExploding):
            self.display.blit(self.image, self.rect.topleft + x)

    def update(self, dt):
        if self.strong and self.isExploding:
            self.animate(dt)
        elif self.ismoving:
            self.move(dt)
            self.animate(dt)

        if self.health <= 0:
            self.get_killed()

    def get_killed(self):
        Enemy.number_eneimes -= 1
        if self.strong:
            quantity = self.calculate_gold_reward()
            # print(quantity)
        else:
            quantity = self.calculate_gold_reward()
            # print(quantity)
        gold(self.all_sprites, quantity, self.rect.center)
        die_sound.play()
        self.kill()

    def calculate_gold_reward(self):
        if self.strong:
            return int(96 * (self.round / 1.2))
        return int(64 * (self.round / 1.2))


