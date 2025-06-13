from settings import *
main_menu_sound = pg.mixer.Sound("../sounds/main_menu.mp3")
class Main_Menu:
    def __init__(self,display,gamemanager):
        self.gamemanager = gamemanager
        self.display = display
        self.layout = pg.Surface((WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        #self.layout.fill('blue')
        self.layout_rect = self.layout.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.button1_state = 0
        self.button2_state = 0
        self.mid_button = []
        self.mid_button1_rect =None
        self.buttons_spritesheet = pg.image.load('../sprites/buttons/buttons.png').convert_alpha()
        self.menu_background = pg.image.load('../sprites/menu_background.jpg').convert_alpha()
        self.menu_background_rect = self.menu_background.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.load()
    def load(self):
        self.buttons_spritesheet = pg.image.load('../sprites/buttons/buttons.png').convert_alpha()
        with open('../sprites/buttons/buttons.json') as f:
            data = json.load(f)
        buttons = data['frames']
        def get_button(frame_data):
            rect = frame_data['frame']
            x, y, w, h = rect['x'], rect['y'], rect['w'], rect['h']
            return self.buttons_spritesheet.subsurface(pg.Rect(x, y, w, h))

        self.Button_Red_9Slides = get_button(buttons['Button_Red_9Slides.png'])
        self.Button_Red_9Slides_rect = self.Button_Red_9Slides.get_frect(
            center=(WINDOW_WIDTH / 2,WINDOW_HEIGHT/2))
        self.mid_button.append(get_button(buttons['Button_Blue_3Slides.png']))
        self.mid_button[0] = pg.transform.scale2x(self.mid_button[0])
        self.mid_button.append(get_button(buttons['Button_Hover_3Slides.png']))
        self.mid_button[1] = pg.transform.scale2x(self.mid_button[1])
        self.mid_button.append(get_button(buttons['Button_Blue_3Slides_Pressed.png']))
        self.mid_button[2] = pg.transform.scale2x(self.mid_button[2])
        self.button1_rect = self.mid_button[0].get_frect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2-80))
        self.button2_rect = self.mid_button[0].get_frect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2+50))
       # self.button1_rect = self.mid_button[0].get_frect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2-80))
        #sound
        main_menu_sound.play()
        #TEXT
        self.pixel_font = pg.font.Font('../sprites/fonts/Minecraft.ttf', 60)
        self.start_text = self.pixel_font.render('START' , True , 'white')
        self.start_text_rect = self.start_text.get_frect(center = (WINDOW_WIDTH/2 ,WINDOW_HEIGHT / 2-75 ))
        self.exit_text = self.pixel_font.render('EXIT', True, 'white')
        self.exit_text_rect = self.start_text.get_frect(center=(WINDOW_WIDTH / 2 +35, WINDOW_HEIGHT / 2 +55))
    def input(self):
        pass
    def collision(self):
        if self.button1_rect.collidepoint(pg.mouse.get_pos()):
            self.button1_state = 1
            if pg.mouse.get_pressed()[0]:
                self.button1_state = 2
                self.gamemanager.state = 'game'
        else :
            self.button1_state = 0
        if self.button2_rect.collidepoint(pg.mouse.get_pos()):
            self.button2_state = 1
            if pg.mouse.get_pressed()[0]:
                self.button2_state = 2
                self.gamemanager.running = False
        else :
            self.button2_state = 0
    def draw(self):
       # self.display.blit(self.Button_Red_9Slides,self.Button_Red_9Slides_rect)
        self.display.fill('black')
        self.menu_background.convert_alpha()
        scaled_menu_background = pg.transform.scale(self.menu_background ,(WINDOW_WIDTH,WINDOW_HEIGHT))
        self.display.blit(scaled_menu_background,(0,0))
       #buttons
        self.display.blit(self.mid_button[self.button1_state] ,
                          self.mid_button[self.button1_state].get_frect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2-80)))

        self.display.blit(self.mid_button[self.button2_state],
                          self.mid_button[self.button2_state].get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 +50)))
        self.display.blit(self.start_text,self.start_text_rect)
        self.display.blit(self.exit_text , self.exit_text_rect)
       #buttons collision
        self.collision()
    def update(self):
        self.input()