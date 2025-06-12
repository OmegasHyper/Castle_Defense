from random import randint

from settings import *
from player import *
from sprites import *
from allsprites import *
from Collision_sprites import *
from sprites import * 
from os import*
from archer import Archer
from collisionsprites import CollisionSprites
from enemy import*


class Game:
    def __init__(self,display , gamemanager):
        self.display = display
        self.all_sprites = AllSPrites()
        self.collision_sprites = pg.sprite.Group()
        self.collision_sprites2 = pg.sprite.Group() #for archer_animations
        self.tower_sprites = pg.sprite.Group()
        self.archer = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()

        
        

        self.gamemanager = gamemanager

        # CollisionSprites( (3393.33,1910),(30,40),(255,0,0),(self.all_sprites,self.collision_sprites2)) # for testing the archer animations

        Archer((self.all_sprites,self.archer), (3400.33, 2350),"NT")
        Archer((self.all_sprites,self.archer), (4400, 3370),"ET")
        Archer((self.all_sprites,self.archer), (2372, 3370),"WT")

        self.setup()

    def setup(self):
        map = pytmx.util_pygame.load_pygame('../sprites/map/map.tmx')

        # Load ground layers
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Ground_Sprites(self.all_sprites, image, (x * TILE_SIZE, y * TILE_SIZE))

        for x, y, image in map.get_layer_by_name('Ground2').tiles():
            Ground_Sprites(self.all_sprites, image, (x * TILE_SIZE, y * TILE_SIZE))

        # Load decorative objects
        for obj in map.get_layer_by_name('decos'):
            Sprites(self.all_sprites, obj.image, (obj.x, obj.y))
        # Load tree collision objects
        for obj in map.get_layer_by_name('Trees'):
            # Use the actual tree image for visual representation
            Sprites(self.all_sprites, obj.image, (int(obj.x), int(obj.y)))

            # Create collision surface with correct dimensions (converted to integers)
            width = int(obj.width) -60
            height = int(obj.height)-50
            x = int(obj.x)+40
            y = int(obj.y)+50

            collision_surf = pg.Surface((width, height))
            collision_surf.fill('red')  # This won't be visible, just for debugging
            Collision_sprites(self.collision_sprites, collision_surf, (x, y))
        # Load col++sion objects
        for obj in map.get_layer_by_name('Collisions'):
            # Convert to integers to avoid floating point precision issues
            width = int(obj.width)
            height = int(obj.height)
            x = int(obj.x)
            y = int(obj.y)

            # Skip objects that are too small (might be placement errors)
            if width < 1 or height < 1:
                continue

            collision_surf = pg.Surface((width, height))
            collision_surf.fill('red')
            Collision_sprites(self.collision_sprites, collision_surf, (x, y))
        # Load player spawn point
        for obj in map.get_layer_by_name('Player_waypoint'):
            self.player = Player(self.all_sprites, (obj.x, obj.y), self.collision_sprites)
            Archer((self.all_sprites,self.archer), (obj.x, obj.y), "ST")

        #load goblin houses
        for obj in map.get_layer_by_name('Goblin_House'):
            # Use the actual house image for visual representation
            Sprites(self.all_sprites, obj.image, (int(obj.x), int(obj.y)))

            # Create collision surface with correct dimensions (converted to integers)
            width = int(obj.width)-30
            height = int(obj.height)-80
            x = int(obj.x)+15
            y = int(obj.y)+40

            collision_surf = pg.Surface((width, height))
            collision_surf.fill('red')  # This won't be visible, just for debugging
            Collision_sprites(self.collision_sprites, collision_surf, (x, y))
        for obj in map.get_layer_by_name('Towers'):
            # Use the actual tree image for visual representation
            Sprites((self.all_sprites,self.tower_sprites), obj.image, (int(obj.x+35), int(obj.y+70)))

            # Create collision surface with correct dimensions (converted to integers)
            width = int(obj.width)-80
            height = int(obj.height)-300
            x = int(obj.x)+40
            y = int(obj.y)+190

            collision_surf = pg.Surface((width, height))
            collision_surf.fill('red')  # This won't be visible, just for debugging
            Collision_sprites(self.collision_sprites, collision_surf, (x, y))
            print (obj.x, obj.y)
        for obj in map.get_layer_by_name('Castle'):
            # Use the actual catsle image for scaling
            original_image = obj.image
            new_width = original_image.get_width() *2
            new_height = original_image.get_height()*2
            scaled_image = pg.transform.scale(original_image,(new_width,new_height))
            Sprites(self.all_sprites, scaled_image, (int(obj.x+70), int(obj.y)))

            # Create collision surface with correct dimensions (converted to integers)
            width = int(obj.width)-240
            height = int(obj.height)-260
            x = int(obj.x)+130
            y = int(obj.y)+150

            collision_surf = pg.Surface((width, height))
            collision_surf.fill('red')  # This won't be visible, just for debugging
            Collision_sprites(self.collision_sprites, collision_surf, (x, y))
        self.enemy_waypoints =[]
        for obj in map.get_layer_by_name('Enemy_waypoint'):
            self.enemy_waypoints.append(obj)
        self.enemy_queue = Queue()
        for i in range(waves['1']['weak']):
            rand_waypoint = self.enemy_waypoints[randint(0,3)]
            self.enemy_queue.enqueue(Enemy((self.all_sprites,self.enemy_group), (rand_waypoint.x , rand_waypoint.y),rand_waypoint.name))
            
    def draw_debug_collisions(self):
        """Draw collision boxes for debugging purposes"""
        # Draw player hitbox
        player_debug_rect = self.player.hitbox_rect.copy()
        player_debug_rect.topleft += self.all_sprites.offset
        pg.draw.rect(self.display, 'green', player_debug_rect, 3)

        # Draw collision sprites
        for sprite in self.collision_sprites:
            debug_rect = sprite.rect.copy()
            debug_rect.topleft += self.all_sprites.offset
            pg.draw.rect(self.display, 'red', debug_rect, 2)

        # Show player position as text
        font = pg.font.Font(None, 36)
        pos_text = font.render(f"Player: ({int(self.player.rect.centerx)}, {int(self.player.rect.centery)})", True,
                               'white')
        self.display.blit(pos_text, (10, 10))

        # Show number of collision objects
        collision_count = len(self.collision_sprites)
        count_text = font.render(f"Collision objects: {collision_count}", True, 'white')
        self.display.blit(count_text, (10, 50))
        

    def draw(self):
        self.display.fill('black')

        # Draw sprites
        self.all_sprites.draw(self.player.rect.center)
        for archer in self.archer:
            archer.draw_range(self.display)
        # Add this line to see collision boxes (remove when not debugging)
        # self.draw_debug_collisions()

    def update(self,dt):
        for archer in self.archer:
            archer.update_archer(dt,self.enemy_group)

        Enemy.spawning()
        if Enemy.spawn == True :
            enemy = self.enemy_queue.dequeue()
            if enemy != None :
                enemy.ismoving = True
                Enemy.spawn = False
        self.all_sprites.update(dt)
        self.draw()

