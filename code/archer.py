import os
from Queue import *
from PIL.ImageChops import offset
from arrow import *
from settings import *
from enemy import *

class Archer(pg.sprite.Sprite) :
    def __init__(self,groups,pos,direction = "NT",attack_range =400):
        super().__init__(groups)
        self.Wave_Font = pg.font.Font('../sprites/fonts/Minecraft.ttf', 90)
        self.Wave_text = self.Wave_Font.render("Wave Cleared", True, (240, 240, 240))
        self.frames = None      #store ainamtions for each direction
        self.all_sprites = groups[0]
        self.pos = pos
        self.direction = direction
        self.direction = direction
        self.attack_range = attack_range
        self.load_images()

        self.current_frame = 1
        self.animation_speed = 300
        self.last_update = pg.time.get_ticks()
        self.arching = False

        self.image = self.frames[self.direction][0] # if the archer not in the arching state it will be as the 0 image
        self.rect = self.image.get_frect(center=self.pos)
        #self.archer_queue = Queue()
    def load_images(self):
        self.frames = self.frames = { 'ET':[], 'NT':[],'ST':[],'WT':[]}
        base_path = "../sprites/archers"
        for dir_name in self.frames.keys():
            path = join(base_path, dir_name) # "../sprites/archers/{dir}"
            for folder_path ,sub_folder,file_names in os.walk(path):
                if file_names :
                    for file_name in sorted (file_names,key = lambda name : int(name.split('.')[0])) : # for load images sorted
                        full_path = join(folder_path, file_name)   #"../sprites/archer/{dir}/{file_name}"
                        surf = pg.image.load(full_path).convert_alpha()
                        self.frames[dir_name].append(surf)


    def update_archer(self,dt,enemy_group):
        for enemy in enemy_group:
            print(Enemy.number_eneimes)
            if Enemy.number_eneimes == 0:
                self.arching = False
                print('waveClear')
                #Text = self.Wave_text.get_frect(center=(WINDOW_WIDTH, WINDOW_HEIGHT))
                continue
            if hasattr(enemy,"rect"):
                distance = pg.math.Vector2(self.rect.center).distance_to(enemy.rect.center)
                shoot_direction = pg.Vector2(enemy.rect.center) - pg.Vector2(self.rect.center)
                
                if distance <= self.attack_range:
                    if self.direction == "NT":
                        if shoot_direction.y > 0:
                            continue

                    if self.direction == "ET":
                        if shoot_direction.x < 0:
                            continue

                    if self.direction == "ST":
                        if shoot_direction.y < 0:
                            continue

                    if self.direction == "WT":
                        if shoot_direction.x > 0:
                            continue
                    self.arching = True
                    #self.archer_queue.enqueue(enemy)
                    break
                else:
                    self.arching = False


        if self.arching:
            now = pg.time.get_ticks()
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.current_frame = (self.current_frame -1 + 1 )% (len(self.frames[self.direction])-1)+1 # cuz starting from frame 1 the frame 0 is used for the static state
                self.image = self.frames[self.direction][self.current_frame]
                Arrow(self.direction, self.rect, enemy, self.all_sprites)

        else:
            self.image = self.frames[self.direction][0]
            self.current_frame = 1

    def draw_range(self, surface):
        screen_pos = pg.Vector2(self.rect.center)

        range_surface = pg.Surface((self.attack_range*2 ,self.attack_range*2),pg.SRCALPHA)
        arc_rect = pg.Rect(0,0,self.attack_range*2,self.attack_range*2)
        direction_angle = {'NT':(0.4,2.74),#1.57,2.14
                            'ST':(3.54,5.88),
                            'ET':(5.1,1.17),#5.7,6.28
                            'WT':(1.97,4.31)} #(3.14,3.7)

        start_angle ,end_angle = direction_angle.get(self.direction,(0,6.28))

        surface.blit(range_surface,(screen_pos.x - self.attack_range,screen_pos.y-self.attack_range))
        surface.blit(self.image , self.rect.topleft)


