from settings import *
from allsprites import*

#this class is for the image
class Tower(pg.sprite.Sprite):
    def __init__(self, groups, image, pos):
        super().__init__(groups)
        self.display = pg.display.get_surface()
        self.pos = pos
        self.image = image
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox = self.rect.inflate(-140,-180)
        self.hitbox.top += 10
        self.black_health_rect = pg.Rect(self.pos[0], self.pos[1], 500, 500)
        self.display_offset = AllSprites.offset
        self.health = 110
        self.isBuilding = True
        # Destruction
        self.is_destroyed = False
        self.destroy_timer = 0
        self.destroy_duration = 75
        self.destroyed_image = pg.image.load('../sprites/towers/Tower_destroyed.png').convert_alpha()

    def load_health_bar(self):
        pg.draw.rect(pg.display.get_surface(), 'black',(self.pos[0] + self.display_offset.x, self.pos[1] + self.display_offset.y, 120, 30), 5, 5)
        pg.draw.rect(pg.display.get_surface(), 'red', (self.pos[0] + self.display_offset.x + 5, self.pos[1] + self.display_offset.y +5, self.health, 20))
    
    def update_health(self,dt):
        if self.is_destroyed:
            return

        if self.health <= 0:
            self.image = self.destroyed_image
            self.rect = self.image.get_rect(topleft=self.pos)
            self.is_destroyed = True
            self.hitbox = pg.Rect(0,0,0,0)
            # self.destroy_timer = pg.time.get_ticks()
        else:
            self.load_health_bar()

