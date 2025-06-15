from settings import *
from allsprites import *

# This class is for the image
class Castle(pg.sprite.Sprite):
    def __init__(self, groups, image, pos):
        super().__init__(groups)
        self.display = pg.display.get_surface()
        self.pos = pos
        self.image = image
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox = self.rect.inflate(-240, -260)  # Adjust hitbox dimensions as needed
        self.hitbox.top += 10
        self.black_health_rect = pg.Rect(self.pos[0], self.pos[1], 500, 500)
        self.display_offset = AllSprites.offset
        self.health = 10  # You can set the health value as needed
        self.isBuilding = True
        self.isDead = False
        self.associated_archers = []
    def add_archer(self, archer_sprite):
        if archer_sprite not in self.associated_archers:
            self.associated_archers.append(archer_sprite)
    def load_health_bar(self):
        bar_width = 450
        bar_height = 40
        health_ratio = self.health / 500
        # Calculate position to center at top of the screen with some padding
        screen_width = self.display.get_width()
        x = (screen_width - bar_width) // 2
        y = 20  # 20px from top of the screen

        # Background bar (black border)
        pg.draw.rect(self.display, 'black', (x, y, bar_width, bar_height), border_radius=8)
        # Red health fill based on current health
        pg.draw.rect(self.display, 'red', (x + 4, y + 4, int((bar_width - 8) * health_ratio), bar_height - 8),
                     border_radius=6)
    def update_health(self, dt):
        self.load_health_bar()

        if self.health <= 0:
            for archer in self.associated_archers:
                archer.kill()
            self.kill()
            self.isDead = True
        else:
            self.load_health_bar()
