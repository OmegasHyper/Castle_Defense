import os

from PIL.ImageChops import offset

from settings import *

class Archer(pg.sprite.Sprite) :
    def __init__(self,groups,pos,direction = "NT",attack_range =1150):
        super().__init__(groups)
        # self.image = pg.image.load("../sprites/archers/ST/0.png")
        self.circle = None
        self.frames = None      #store ainamtions for each direction
        # self.arching = None
        # self.last_update = None
        # self.current_frame = None
        # self.animation_speed = None
        self.direction = direction
        self.attack_range = attack_range


        self.load_images()

        self.current_frame = 1
        self.animation_speed = 150
        self.last_update = pg.time.get_ticks()
        self.arching = False

        self.image = self.frames[self.direction][0]
        self.rect = self.image.get_frect(center=pos)


    # def load_animation_frames(self):
    #     self.frames = { 'ET':[], 'NT':[],'ST':[],'WT':[]}
    #     self.load_images()
    #     self.current_frame =1
    #     self.animation_speed = 150
    #     self.last_update = pg.time.get_ticks()
    #     self.arching = False
    #
    #     # for direction in directions:
    #     #     path = f"../sprites/archers/{direction}"
    #     #     for filename in sorted(os.listdir(path)):
    #     #         pass

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



    def update(self,dt,enemy_group):
        for enemy in enemy_group:
            if hasattr(enemy,"rect"):
                distance = pg.math.Vector2(self.rect.center).distance_to(enemy.rect.center)
                if distance <= self.attack_range:
                    self.arching = True
                    break


        if self.arching:
            now = pg.time.get_ticks()
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.current_frame = (self.current_frame -1 + 1 )% (len(self.frames[self.direction])-1)+1 # cuz starting from frame 1 the frame 0 is used for the static state
                self.image = self.frames[self.direction][self.current_frame]

        else:
            self.image = self.frames[self.direction][0]
            self.current_frame = 1

    def draw(self, surfacet):
        #pos = self.rect.center+offset
        # self.circle =none\
        pg.draw.circle(surface,"red", self.rect.center,self.attack_range,1)
        # pg.draw.circle(surface,"white",(0,255,0), self.rect.center ,self.attack_range,1)
        # self.circle.fill('white')




