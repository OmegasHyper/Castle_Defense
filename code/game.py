from random import randint
from settings import *
from player import *
from sprites import *
from allsprites import *
from Collision_sprites import *
from sprites import * 
#from os import*      os has open() that overrides json.open()
from archer import Archer
from enemy import*
from Tower import *
from Castle import *
from Obstacles import *
from Stack import *

wingame_sound = pg.mixer.Sound("../sounds/win.wav")
button_hover_sound = pg.mixer.Sound("../sounds/button_hover.wav")
button_click_sound = pg.mixer.Sound("../sounds/button_click.mp3")
gold_quantity = 1000
outer_archers = []
class Game:
    def __init__(self,display , gamemanager):
        # self.gold_sprite = pg.image.load("../sprites/map/Resources/Resources/G_Idle_(NoShadow).png").convert_alpha()
        # self.gold_sprite = pg.transform.smoothscale(self.gold_sprite, (100, 100))
        self.tower_dict = {}
        
        self.display = display
        self.all_sprites = AllSprites()
        self.collision_sprites = pg.sprite.Group()
        self.collision_sprites2 = pg.sprite.Group() #for archer_animations
        self.building_sprites = pg.sprite.Group()
        self.archer = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()

        self.Obstacles_spr = pg.sprite.Group()
        self.gamemanager = gamemanager
        self.round = 1
        self.stack_obst = Stack_obstacles()
        
        self.pause_button_state = 0
        self.shop_button_state = 0
        self.mid_button = []
        self.isButton1hovered = False
        self.isButton2hovered = False

        self.setup()

    def setup(self):
        global outer_archers
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

        # Load collision objects
        for obj in map.get_layer_by_name('Collisions'):
            # global gold_quantity
           
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
        #load goblin houses
        for obj in map.get_layer_by_name('Goblin_House'):
            # Use the actual house image for visual representation
            Sprites(self.all_sprites, obj.image, (int(obj.x), int(obj.y)))

            # Create collision surface with correct dimensions (converted to integers)
            width = int(obj.width)-30
            height = int(obj.height)-80
            x = int(obj.x)+15
            y = int(obj.y)+40


        # self.tower_dict = {}
        for obj in map.get_layer_by_name('Towers'):
            tower_name = obj.name
            # Use the actual Tower image for visual representation
            tower_instance =Tower((self.all_sprites, self.building_sprites), obj.image, (int(obj.x+35), int(obj.y+70)))
            self.tower_dict[tower_name] = tower_instance
            # Create collision surface with correct dimensions (converted to integers)
            width = int(obj.width)-80
            height = int(obj.height)-300
            x = int(obj.x)+40
            y = int(obj.y)+190

        for obj in map.get_layer_by_name('Castle'):
            # Create collision surface with correct dimensions (converted to integers)
            print(obj.name)
            width = int(obj.width) - 80
            height = int(obj.height) - 300
            x = int(obj.x) + 40
            y = int(obj.y) + 190
            # Use the actual castle image for scaling
            original_image = obj.image
            new_width = original_image.get_width() * 2
            new_height = original_image.get_height() * 2
            scaled_image = pg.transform.scale(original_image, (new_width, new_height))

            # Create an instance of the Castle class
            castle_instance = Castle((self.all_sprites, self.building_sprites), scaled_image,
                                     (int(obj.x + 70), int(obj.y)))
            self.tower_dict[obj.name] = castle_instance  # Store the castle instance in the dictionary
        for obj in map.get_layer_by_name('Outer_archers_waypoints'):
            tower_name = obj.name
            parent_tower = self.tower_dict[tower_name]
            outer_archers.append(Archer((self.all_sprites, self.archer), (obj.x, obj.y), tower_name,parent_tower=parent_tower))
        for obj in map.get_layer_by_name('Inner_archers_waypoints'):
            archer_instance=  Archer((self.all_sprites, self.archer), (obj.x, obj.y), obj.name)
            castle_instance = self.tower_dict["Castle"]
            castle_instance.add_archer(archer_instance)
        self.enemy_waypoints =[]
        for obj in map.get_layer_by_name('Enemy_waypoint'):
            self.enemy_waypoints.append(obj)
        self.enemy_queue = Queue()

        buttons_spritesheet = pg.image.load('../sprites/buttons/buttons.png').convert_alpha()
        with open('../sprites/buttons/buttons.json') as f:
            data = json.load(f)
        buttons = data['frames']
        def get_button(frame_data):
            rect = frame_data['frame']
            x, y, w, h = rect['x'], rect['y'], rect['w'], rect['h']
            return buttons_spritesheet.subsurface(pg.Rect(x, y, w, h))
        self.mid_button.append(get_button(buttons['Button_Blue_3Slides.png']))
        self.mid_button[0] = pg.transform.smoothscale(self.mid_button[0], (130, 70))
        self.mid_button.append(get_button(buttons['Button_Hover_3Slides.png']))
        self.mid_button[1] = pg.transform.smoothscale(self.mid_button[1], (130, 70))
        self.mid_button.append(get_button(buttons['Button_Blue_3Slides_Pressed.png']))
        self.mid_button[2] = pg.transform.smoothscale(self.mid_button[2], (130, 70))
        self.pause_button_rect = self.mid_button[self.pause_button_state].get_frect(center = (WINDOW_WIDTH - 100, 60))
        self.shop_button_rect = self.mid_button[self.shop_button_state].get_frect(center = (WINDOW_WIDTH - 280, 60))

        # Text
        self.pixel_font = pg.font.Font('../sprites/fonts/Minecraft.ttf', 30)
        self.pause_text = self.pixel_font.render('Pause' , True , 'white')
        self.pause_text_rect = self.pause_text.get_frect(center = self.pause_button_rect.center)
        self.shop_text = self.pixel_font.render('Shop', True, 'white')
        self.shop_text_rect = self.shop_text.get_frect(center = self.shop_button_rect.center)
        # self.round_text = self.pixel_font.render(f'Wave: {self.round}', True, 'white')
        # self.round_text_rect = self.round_text.get_frect(center = (WINDOW_WIDTH / 2, 80))

        
        #self.gold_sprite_rect = self.gold_text.get_frect(midright=(self.gold_text_rect.midleft))
        #self.gold_sprite_rect.x -= 63
        #self.gold_sprite_rect.y -= 48

        # create first round 
        self.create_round(self.round)
    def collision(self):
        if self.pause_button_rect.collidepoint(pg.mouse.get_pos()):
            self.pause_button_state = 1
            if not self.isButton1hovered:
                button_hover_sound.play()
                self.isButton1hovered = True
            if pg.mouse.get_pressed()[0]:
                button_click_sound.play()
                self.pause_button_state = 2
                self.gamemanager.state = 'pause'
        else :
            self.isButton1hovered = False
            self.pause_button_state = 0

        if self.shop_button_rect.collidepoint(pg.mouse.get_pos()):
            self.shop_button_state = 1
            if not self.isButton2hovered:
                button_hover_sound.play()
                self.isButton2hovered = True
            if pg.mouse.get_pressed()[0]:
                button_click_sound.play()
                self.shop_button_state = 2
                self.gamemanager.state = 'shop'
        else :
            self.shop_button_state = 0
            self.isButton2hovered = False

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

        
        self.display.blit(self.mid_button[self.pause_button_state], self.pause_button_rect)
        self.display.blit(self.mid_button[self.shop_button_state], self.shop_button_rect)
        self.display.blit(self.shop_text,self.shop_text_rect)
        self.display.blit(self.pause_text , self.pause_text_rect)
        round_bg_rect = self.round_text_rect.inflate(30, 15)
        pg.draw.rect(self.display, (54, 151, 247), round_bg_rect, border_radius=10)
        pg.draw.rect(self.display, (0, 81, 186), round_bg_rect, width=5, border_radius=10)
        self.display.blit(self.round_text, self.round_text_rect)

        gold_quantity_text = f'Gold: {gold_quantity}'
        self.gold_text = self.pixel_font.render(gold_quantity_text, True, (240, 240, 240))
        self.gold_text_rect = self.gold_text.get_frect(center = (130, 50) )
        pg.draw.rect(self.display, (0, 81, 186), self.gold_text_rect.inflate(17, 12).move(0, -5), 0, 10)
        pg.draw.rect(self.display, (54, 151, 247), self.gold_text_rect.inflate(10, 5).move(0, -5), 0, 10)
        self.display.blit(self.gold_text, self.gold_text_rect)
        # self.display.blit(self.gold_sprite, self.gold_sprite_rect)

        #self.draw_debug_collisions()
    def create_round(self,round):
        r = str(self.round)
        counter_weak = 0
        counter_strong = 0
        
        for i in range(waves[r]['weak']+waves[r]['strong']):
            which_create = randint(0,1)
            if (which_create and counter_weak < waves[r]['weak']) or  counter_strong ==  (waves[r]['strong']):    
                rand_waypoint = self.enemy_waypoints[randint(0,3)]
                self.enemy_queue.enqueue(Enemy((self.all_sprites,self.enemy_group), (rand_waypoint.x , rand_waypoint.y),rand_waypoint.name,(self.building_sprites,self.Obstacles_spr),False, self.round))
                counter_weak += 1
            else : 
                    rand_waypoint = self.enemy_waypoints[randint(0,3)]
                    self.enemy_queue.enqueue(Enemy((self.all_sprites,self.enemy_group), (rand_waypoint.x , rand_waypoint.y),rand_waypoint.name,(self.building_sprites,self.Obstacles_spr),True, self.round))
                    counter_strong +=1
                
        Enemy.spawn_time = waves [r]['spawn_time']
        print(f"round {r} created")
        if r =='3' : print(Enemy.total_eneimes)         ## debugging purpose
        self.round_text = self.pixel_font.render(f'Wave: {self.round}', True, 'white')
        self.round_text_rect = self.round_text.get_frect(center=(WINDOW_WIDTH / 2, 90))
        self.round+=1
    time_start_wait =0
    get_time = True
    def wait (self,time, time_start_wait):
        time_to_stop = time
        first_time = time_start_wait
        delay =pg.time.get_ticks()
        if delay - first_time > time_to_stop:
            return False
        else: 
            return True 
    def reset(self):
        global gold_quantity
        gold_quantity = 2000
    def update(self,dt):
        for archer in self.archer:
            archer.update_archer(dt,self.enemy_group)
        # spawn of eneimes 
        Enemy.spawning()
        if Enemy.spawn == True :
            enemy = self.enemy_queue.dequeue()
            if enemy != None :
                enemy.ismoving = True
                Enemy.spawn = False
        # timer for waves 
        if not self.enemy_queue.get_size() :
            if Game.get_time:
                Game.time_start_wait = pg.time.get_ticks()
                Game.get_time = False
            create = not self.wait(10000,Game.time_start_wait)      ## the timer is changable for debuging it has to be from levels table
            if create and self.round > 3:
                print("round finished")
                self.gamemanager.state = "wingame"
                wingame_sound.play()
            if create and self.round <= 3:
                self.create_round(self.round)
                
                Game.get_time = True

        put_obst(self.all_sprites, self.Obstacles_spr,self.stack_obst)
        check_undo(self.stack_obst)

            # Obstacles((self.all_sprites, self.Obstacles_spr), (3400, 5000))
        self.all_sprites.update(dt)
        self.collision()
        self.draw()
        castle_instance = self.tower_dict["Castle"]
        if  castle_instance.isDead :
            self.gamemanager.allowIngamesound = False
            castle_instance.play_gameover()
            self.gamemanager.state= "gameover"


        for building in self.building_sprites:
            building.update_health(dt)

        


