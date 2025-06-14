from pause_menu import button_hover_sound , button_click_sound
from settings import *

class ShopMenu:
    def __init__(self,display,game_manager):
        self.display = display
        self.game_manager = game_manager
        self.resume_button_state = 0
        self.level1_button_state = 0
        self.level2_button_state = 0
        self.level3_button_state = 0
        self.mid_button = []
        self.display_copy = display.copy()
        self.scale = 0.2
        small_size = (int(WINDOW_WIDTH*self.scale),int(WINDOW_HEIGHT*self.scale))

        self.blurred = pg.transform.smoothscale(self.display_copy,small_size)
        self.blurred = pg.transform.smoothscale(self.blurred,(WINDOW_WIDTH,WINDOW_HEIGHT))
        self.overlay = pg.Surface((WINDOW_WIDTH,WINDOW_HEIGHT),pg.SRCALPHA)
        self.overlay.fill((0 , 0, 0,150))

        self.pixel_font = pg.font.Font('../sprites/fonts/Minecraft.ttf',60)
        self.shop_text = self.pixel_font.render("shop",True,(210,210,210))
        self.shop_text_rect = self.shop_text.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.button_setup()
        self.isLevel1hovered = False
        self.isLevel2Hovered = False
        self.isLevel3Hovered = False
        self.isResumeHovered = False

    def button_setup(self):
        buttons_spritesheet = pg.image.load('../sprites/buttons/buttons.png').convert_alpha()
        with open('../sprites/buttons/buttons.json') as f:
            data = json.load(f)
        buttons = data['frames']
        def get_button(frame_data):
            rect = frame_data['frame']
            x,y,w,h =rect['x'] ,rect['y'],rect['w'],rect['h']
            return buttons_spritesheet.subsurface(pg.Rect(x,y,w,h))

        self.mid_button.append(get_button(buttons['Button_Blue_3Slides.png']))
        self.mid_button[0] = pg.transform.smoothscale(self.mid_button[0],(130,70))
        self.mid_button.append(get_button(buttons['Button_Hover_3Slides.png']))
        self.mid_button[1] = pg.transform.smoothscale(self.mid_button[1], (130, 70))
        self.mid_button.append(get_button(buttons['Button_Blue_3Slides_Pressed.png']))
        self.mid_button[2] = pg.transform.smoothscale(self.mid_button[2], (130, 70))


        self.resume_button_rect = self.mid_button[self.resume_button_state].get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2 + 200))
        self.level1_button_rect = self.mid_button[self.level1_button_state].get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2 - 140))
        self.level2_button_rect = self.mid_button[self.level2_button_state].get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2 - 70))
        self.level3_button_rect = self.mid_button[self.level3_button_state].get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2 ))

        self.pixel_font = pg.font.Font('../sprites/fonts/Minecraft.ttf',25)
        self.resume_text = self.pixel_font.render("resume",True,(255,255,255))
        self.resume_text_rect =self.resume_text.get_rect(center=self.resume_button_rect.center)
        self.level1_text = self.pixel_font.render("level 1",True,('white'))
        self.level1_text_rect = self.level1_text.get_rect(center = self.level1_button_rect.center)
        self.level2_text = self.pixel_font.render("level 2",True,('white'))
        self.level2_text_rect = self.level2_text.get_rect(center = self.level2_button_rect.center)
        self.level3_text = self.pixel_font.render("level 3",True,('white'))
        self.level3_text_rect = self.level3_text.get_rect(center = self.level3_button_rect.center)


    def update(self):
        self.display.blit(self.blurred, (0,0))
        self.display.blit(self.overlay, (0,0))


        self.collision()
        self.display.blit(self.mid_button[self.resume_button_state],self.resume_button_rect)
        # self.display.blit(self.resume_text,self.resume_text_rect)

        self.display.blit(self.mid_button[self.level1_button_state],self.level1_button_rect)
        # self.display.blit(self.level1_text,self.level2_button_rect)

        self.display.blit(self.mid_button[self.level2_button_state],self.level2_button_rect)
        # self.display.blit(self.level2_text,self.level3_button_rect)

        self.display.blit(self.mid_button[self.level3_button_state],self.level3_button_rect)
        # self.display.blit(self.level3_text,self.level3_button_rect)


        self.display.blit(self.resume_text, self.resume_text_rect)
        self.display.blit(self.level1_text, self.level1_text_rect)
        self.display.blit(self.level2_text, self.level2_text_rect)
        self.display.blit(self.level3_text, self.level3_text_rect)

    def collision(self):
        if self.resume_button_rect.collidepoint(pg.mouse.get_pos()):
            self.resume_button_state = 1
            if not self.isResumeHovered:
                button_hover_sound.play()
                self.isResumeHovered = True
            if pg.mouse.get_just_pressed()[0]:
                button_click_sound.play()
                self.resume_button_state = 2
                self.game_manager.state = 'game'

        else:
            self.isResumeHovered = False
            self.resume_button_state = 0


        if self.level1_button_rect.collidepoint(pg.mouse.get_pos()):
            self.level1_button_state = 1
            if not self.isLevel1Hovered:
                button_hover_sound.play()
                self.isLevel1Hovered = True

            if pg.mouse.get_just_pressed()[0]:
                button_click_sound.play()
                self.level1_button_state = 2
                self.game_manager.state = 'game'

        else :
            self.level1_button_state = 0
            self.isLevel1Hovered = False



        if self.level2_button_rect.collidepoint(pg.mouse.get_pos()):
            self.level2_button_state = 1
            if not self.isLevel2Hovered:
                button_hover_sound.play()
                self.isLevel2Hovered = True
                # self.game_manager.state = 'game'
            if pg.mouse.get_just_pressed()[0]:
                button_click_sound.play()
                self.level2_button_state = 2
                self.game_manager.state = 'game'

        else :
            self.level2_button_state = 0
            self.isLevel2Hovered = False




        if self.level3_button_rect.collidepoint(pg.mouse.get_pos()):
            self.level3_button_state = 1
            if not self.isLevel3Hovered:
                button_hover_sound.play()
                self.isLevel3Hovered = True
                # self.game_manager.state = 'game'
            if pg.mouse.get_just_pressed()[0]:
                button_click_sound.play()
                self.level3_button_state = 2
                self.game_manager.state = 'game'

        else :
            self.level3_button_state = 0
            self.isLevel3Hovered = False







