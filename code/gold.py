from settings import *
import game
class gold(pg.sprite.Sprite):
    def __init__(self, groups, quantity, pos):
        super().__init__(groups)
        self.sprite_sheet = pg.image.load("../sprites/map/Resources/Resources/G_Spawn.png").convert_alpha()
        self.idle_sprite = pg.image.load("../sprites/map/Resources/Resources/G_Idle.png").convert_alpha()
        self.sprite_width = 128
        self.sprite_height = 128
        self.auto_collect_time = 3000
        self.frame_index = 0
        self.quantity = quantity
        self.frames = []
        for i in range(7):
            frame = self.get_sprite(self.sprite_sheet, x=i * self.sprite_width, y=0,
                                     width=self.sprite_width, height=self.sprite_height)
            self.frames.append(frame)

        self.image = self.frames[0]
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pg.time.get_ticks()
        self.frame_time = 60
        self.last_frame_time = self.start_time

    def get_sprite(self, sheet, x, y, width, height):
        sprite = pg.Surface((width, height), pg.SRCALPHA)
        sprite.blit(sheet, (0, 0), (x, y, width, height))
        return sprite
    
    def update(self, dt):
        current_time = pg.time.get_ticks()
        if current_time - self.last_frame_time >= self.frame_time:
            self.last_frame_time = pg.time.get_ticks()
            if self.frame_index < len(self.frames) and current_time - self.start_time <= self.auto_collect_time:
                self.image = self.frames[self.frame_index]
                self.frame_index += 1
            elif current_time - self.start_time <= self.auto_collect_time:
                self.image = self.idle_sprite
            elif self.frame_index > 0 :
                self.frame_index -= 1 
                self.image = self.frames[self.frame_index]
            else:
                # print(f"{self.quantity} Gold collected")
                game.gold_quantity += self.quantity
                print(game.gold_quantity)
                self.kill()