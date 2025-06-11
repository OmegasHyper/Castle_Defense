from settings import *
#from ground import collisionsprites

class Player(pg.sprite.Sprite):
    def __init__(self,groups,pos,collision_sprites):
        super().__init__(groups)
        self.image = pg.image.load("../sprites/player/walk/tile000.png")
        self.rect = self.image.get_frect(center=pos)
        self.collision_sprites = collision_sprites
        self.hitbox_rect = self.rect.inflate(-150,-150)
        self.speed = 500
        self.direction = pg.Vector2()

    def input(self):
        keys = pg.key.get_pressed()
        self.direction.x = int(keys[pg.K_d]) - int(keys[pg.K_a])
        self.direction.y = int(keys[pg.K_s]) - int(keys[pg.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
    def collision(self , direction):
        for sprite in self.collision_sprites:
            #if pygame.sprite.spritecollide(self,self.collision_sprites,False,pygame.sprite.collide_mask):
            if sprite.rect.colliderect(self.hitbox_rect):
                if(direction == 'x'):
                    if self.direction.x > 0 : self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0 : self.hitbox_rect.top = sprite.rect.bottom
                self.rect.center = self.hitbox_rect.center
    def move(self,dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('x')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('y')
        self.rect.center = self.hitbox_rect.center
    def update(self,dt):
        self.input()
        self.move(dt)


