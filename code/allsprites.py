from settings import *

class AllSPrites(pg.sprite.Group):
    offset = pg.Vector2()
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
    def draw(self , target_pos):
        AllSPrites.offset.x = 1280 / 2 - target_pos[0] # Show tile area
        AllSPrites.offset.y = 720 / 2 - target_pos[1]
        ground_sprites = [sprite for sprite in self if hasattr(sprite , 'ground' )]
        object_sprites = [sprite for sprite in self if not hasattr(sprite , 'ground' ) ]
        enemy_sprites  = [sprite for sprite in self if hasattr(sprite , 'enemy') and not hasattr(sprite, 'ground') ]
        archers_sprites = [sprite for sprite in self if not hasattr(sprite , 'ground' ) and hasattr(sprite , 'isArcher')]
        for layer in [ground_sprites,object_sprites,archers_sprites, enemy_sprites]:#the order is important
            for sprite in sorted(layer,key  = lambda sprite: sprite.rect.centery):
                #print(sprite)
                if  hasattr(sprite , 'enemy') and not hasattr(sprite, 'ground') :
                    if sprite.ismoving:
                        sprite.draw(AllSPrites.offset)
                    else :continue
                else :
                    self.display_surface.blit(sprite.image,sprite.rect.topleft + AllSPrites.offset)
