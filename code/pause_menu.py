from settings import *
button_hover_sound = pg.mixer.Sound("../sounds/button_hover.wav")
button_click_sound = pg.mixer.Sound("../sounds/button_click.mp3")
class Pause_menu:
    def __init__(self, display, game_manager):
        self.display = display
        self.game_manager = game_manager
        self.resume_button_state = 0
        self.menu_button_state = 0
        self.mid_button = []
        self.display_copy = display.copy()
        self.scale = 0.2
        small_size = (int(WINDOW_WIDTH * self.scale), int(WINDOW_HEIGHT * self.scale))
        self.blurred = pg.transform.smoothscale(self.display_copy, small_size)
        self.blurred = pg.transform.smoothscale(self.blurred, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.overlay = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA)
        self.overlay.fill((0, 0, 0, 150))
        self.pixel_font = pg.font.Font('../sprites/fonts/Minecraft.ttf', 60)
        self.pause_text = self.pixel_font.render("Paused", True, (210, 210, 210))
        self.pause_text_rect = self.pause_text.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.button_setup()
        self.isButton1hovered = False
        self.isButton2hovered = False
    def button_setup (self):
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
        self.resume_button_rect = self.mid_button[self.resume_button_state].get_frect(center = (WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) -70))
        self.menu_button_rect = self.mid_button[self.menu_button_state].get_frect(center = (WINDOW_WIDTH/2, (WINDOW_HEIGHT/2) +70))

        self.pixel_font = pg.font.Font('../sprites/fonts/Minecraft.ttf', 25)
        self.resume_text = self.pixel_font.render('Resume' , True , 'white')
        self.resume_text_rect = self.resume_text.get_frect(center = self.resume_button_rect.center)
        self.menu_text = self.pixel_font.render('Menu', True, 'white')
        self.menu_text_rect = self.menu_text.get_frect(center=self.menu_button_rect.center)

    def update(self):
        self.display.blit(self.blurred, (0, 0))
        self.display.blit(self.overlay, (0, 0))
        self.display.blit(self.resume_text, self.resume_text_rect)
        self.display.blit(self.menu_text, self.menu_text_rect)

        self.collision()
        self.display.blit(self.mid_button[self.resume_button_state], self.resume_button_rect)
        self.display.blit(self.resume_text , self.resume_text_rect)
        self.display.blit(self.mid_button[self.menu_button_state], self.menu_button_rect)
        self.display.blit(self.menu_text, self.menu_text_rect)

    def collision(self):
        if self.resume_button_rect.collidepoint(pg.mouse.get_pos()):
            self.resume_button_state = 1
            if not self.isButton1hovered:
                self.isButton1hovered = True
            if pg.mouse.get_just_pressed()[0]:
                button_click_sound.play()
                self.resume_button_state = 2
                self.game_manager.state = 'game'
                # print(self.game_manager.state)
        else :
            self.isButton1hovered = False
            self.resume_button_state = 0

        if self.menu_button_rect.collidepoint(pg.mouse.get_pos()):
            self.menu_button_state = 1
            if not self.isButton2hovered:
                self.isButton2hovered = True

            if pg.mouse.get_pressed()[0]:
                button_click_sound.play()
                self.menu_button_state = 2
                self.game_manager.state = 'menu'
        else :
            self.menu_button_state = 0
            self.isButton2hovered = False