from settings import *

class AllSPrites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.offset = pg.Vector2()
    def draw(self , target_pos):
        self.offset.x = 1280 / 2 - target_pos[0] # Show tile area
        self.offset.y = 720 / 2 - target_pos[1]
        ground_sprites = [sprite for sprite in self if hasattr(sprite , 'ground' )]
        object_sprites = [sprite for sprite in self if not hasattr(sprite , 'ground' )]
        for layer in [ground_sprites,object_sprites]:#the order is important
            for sprite in sorted(layer,key  = lambda sprite: sprite.rect.centery):
                #print(sprite)
                self.display_surface.blit(sprite.image,sprite.rect.topleft + self.offset)