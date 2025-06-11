from settings import *
from player import *
from sprites import *
from allsprites import *
from Collision_sprites import *
from sprites import *
class Game:
    def __init__(self,display , gamemanager):
        self.display = display
        self.all_sprites = AllSPrites()
        self.collision_sprites = pg.sprite.Group()
        self.gamemanager = gamemanager
        self.player = Player(self.all_sprites)
        self.setup()

    def setup(self):
        map = pytmx.util_pygame.load_pygame('../sprites/map/map.tmx')
        for x,y , image in map.get_layer_by_name('Ground').tiles():
            print(image)
            Ground_Sprites(self.all_sprites, image ,(x*TILE_SIZE,y*TILE_SIZE))
        for x, y, image in map.get_layer_by_name('Ground2').tiles():
            Ground_Sprites(self.all_sprites, image, (x * TILE_SIZE, y * TILE_SIZE))
        for obj in map.get_layer_by_name('Trees'):
            Collision_sprites((self.all_sprites, self.collision_sprites), obj.image, (obj.x , obj.y ))
        for obj in map.get_layer_by_name('Collisions'):
            Collision_sprites( self.collision_sprites, pg.Surface((obj.x , obj.y)), (obj.x , obj.y ))
        for obj in map.get_layer_by_name('decos'):
            print(obj.image)
            Sprites((self.all_sprites, self.collision_sprites), obj.image, (obj.x , obj.y ))
    def update(self,dt):
        self.player.update(dt)
    def draw (self):
        self.display.fill('black')

        # Draw sprites
        self.all_sprites.draw(self.player.rect.center)

