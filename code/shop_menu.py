from pause_menu import button_hover_sound , button_click_sound
from settings import *
from game import outer_archers
import game
# outer_archers : south, west, north, east
class ShopMenu:
    def __init__(self,display,game_manager):
        self.display = display
        self.game_manager = game_manager
        # self.gold_quantity = game.gold_quantity
        # self.archers = archers
        self.tower_level = {
            'NT' : 1,
            'WT' : 1,
            'ET' : 1,
            'ST' : 1
        }
        self.resume_button_state = 0
        self.NT_button_state = 0
        self.ST_button_state = 0
        self.ET_button_state = 0
        self.WT_button_state = 0
        self.mid_button = []

        self.overlay = pg.Surface((WINDOW_WIDTH,WINDOW_HEIGHT),pg.SRCALPHA)
        self.overlay.fill((0 , 0, 0,150))

        self.pixel_font = pg.font.Font('../sprites/fonts/Minecraft.ttf',60)
        self.shop_text = self.pixel_font.render("shop",True,(210,210,210))
        self.shop_text_rect = self.shop_text.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        
        self.button_setup()
        
        self.isNTHovered = False
        self.isSTHovered = False
        self.isETHovered = False
        self.isWTHovered = False
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
        self.mid_button[0] = pg.transform.smoothscale(self.mid_button[0],(170,85))
        self.mid_button.append(get_button(buttons['Button_Hover_3Slides.png']))
        self.mid_button[1] = pg.transform.smoothscale(self.mid_button[1], (170, 85))
        self.mid_button.append(get_button(buttons['Button_Blue_3Slides_Pressed.png']))
        self.mid_button[2] = pg.transform.smoothscale(self.mid_button[2], (170, 85))


        self.NT_button_rect = self.mid_button[self.NT_button_state].get_frect(center=(400, 200))
        self.ST_button_rect = self.mid_button[self.ST_button_state].get_frect(center=(900, 200))
        self.ET_button_rect = self.mid_button[self.ET_button_state].get_frect(center=(400, 480))
        self.WT_button_rect = self.mid_button[self.WT_button_state].get_frect(center=(900, 480))
        self.resume_button_rect = self.mid_button[self.resume_button_state].get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 90))

        self.pixel_font = pg.font.Font('../sprites/fonts/Minecraft.ttf',25)
        self.resume_text = self.pixel_font.render("resume",True,(255,255,255))
        self.resume_text_rect =self.resume_text.get_rect(center=self.resume_button_rect.center)
        self.NT_text = self.pixel_font.render("Upgrade",True,'white')
        self.NT_text_rect = self.NT_text.get_rect(center = self.NT_button_rect.center)
        self.ST_text = self.pixel_font.render("Upgrade",True,'white')
        self.ST_text_rect = self.ST_text.get_rect(center = self.ST_button_rect.center)
        self.ET_text = self.pixel_font.render("Upgrade",True,'white')
        self.ET_text_rect = self.ET_text.get_rect(center = self.ET_button_rect.center)
        self.WT_text = self.pixel_font.render("Upgrade",True,'white')
        self.WT_text_rect = self.WT_text.get_rect(center = self.WT_button_rect.center)

        self.upgrade_info_text = self.pixel_font.render('info: Upgrades increase tower (range, damage, fire rate)', True, (230, 230, 230))
        self.upgrade_info_text_rect = self.upgrade_info_text.get_rect(center = (WINDOW_WIDTH/2, 50))
    def update(self):
        self.display.fill((54, 151, 247))
        self.display.blit(self.overlay, (0,0))


        self.collision()
        self.display.blit(self.mid_button[self.resume_button_state],self.resume_button_rect)
        self.display.blit(self.mid_button[self.NT_button_state],self.NT_button_rect)
        self.display.blit(self.mid_button[self.ST_button_state],self.ST_button_rect)
        self.display.blit(self.mid_button[self.ET_button_state],self.ET_button_rect)
        self.display.blit(self.mid_button[self.WT_button_state],self.WT_button_rect)

        self.display.blit(self.resume_text, self.resume_text_rect)
        self.display.blit(self.NT_text, self.NT_text_rect)
        self.display.blit(self.ST_text, self.ST_text_rect)
        self.display.blit(self.ET_text, self.ET_text_rect)
        self.display.blit(self.WT_text, self.WT_text_rect)

        if self.tower_level['NT'] == 3:
            self.NT_current_text = self.pixel_font.render(f'North tower level: {self.tower_level['NT']} (Max)', True, (230, 230, 230))
        else:
            self.NT_current_text = self.pixel_font.render(f'North tower level: {self.tower_level['NT']}', True, (230, 230, 230))
        if self.tower_level['ST'] == 3:
            self.ST_current_text = self.pixel_font.render(f'South tower level: {self.tower_level['ST']} (Max)', True, (230, 230, 230))
        else:
            self.ST_current_text = self.pixel_font.render(f'South tower level: {self.tower_level['ST']}', True, (230, 230, 230))
        if self.tower_level['ET'] == 3:
            self.ET_current_text = self.pixel_font.render(f'East tower level: {self.tower_level['ET']} (Max)', True, (230, 230, 230))
        else:
            self.ET_current_text = self.pixel_font.render(f'East tower level: {self.tower_level['ET']}', True, (230, 230, 230))
        if self.tower_level['WT'] == 3:
            self.WT_current_text = self.pixel_font.render(f'West tower level: {self.tower_level['WT']} (Max)', True, (230, 230, 230))
        else:
            self.WT_current_text = self.pixel_font.render(f'West tower level: {self.tower_level['WT']}', True, (230, 230, 230))

        self.NT_current_text_rect = self.NT_current_text.get_rect(center = (400, 150))
        self.ST_current_text_rect = self.ST_current_text.get_rect(center = (900, 150))
        self.ET_current_text_rect = self.ET_current_text.get_rect(center = (400, 430))
        self.WT_current_text_rect = self.WT_current_text.get_rect(center = (900, 430))
        
        self.gold_quantity_text = self.pixel_font.render(f"Gold: {game.gold_quantity}", True, 'white')
        self.gold_quantity_text_rect = self.gold_quantity_text.get_rect(center = (120, 120))

        self.display.blit(self.NT_current_text, self.NT_current_text_rect)
        self.display.blit(self.ST_current_text, self.ST_current_text_rect)
        self.display.blit(self.ET_current_text, self.ET_current_text_rect)
        self.display.blit(self.WT_current_text, self.WT_current_text_rect)

        self.display.blit(self.upgrade_info_text, self.upgrade_info_text_rect)
        self.display.blit(self.gold_quantity_text, self.gold_quantity_text_rect)

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


        if self.NT_button_rect.collidepoint(pg.mouse.get_pos()):
            self.NT_button_state = 1
            if not self.isNTHovered:
                button_hover_sound.play()
                self.isNTHovered = True

            if pg.mouse.get_just_pressed()[0]:
                button_click_sound.play()
                self.NT_button_state = 2
                if game.gold_quantity >= Tower_upgrades[f'level{self.tower_level['NT']}']['cost'] and self.tower_level['NT'] < 3:
                    game.gold_quantity -= Tower_upgrades[f'level{self.tower_level['NT']}']['cost']
                    self.tower_level['NT'] += 1
                    outer_archers[2].attack_range = Tower_upgrades[f'level{self.tower_level['NT']}']['range']
                    outer_archers[2].damage = Tower_upgrades[f'level{self.tower_level['NT']}']['dmg']
                    outer_archers[2].animation_speed = Tower_upgrades[f'level{self.tower_level['NT']}']['fire_rate']

        else :
            self.NT_button_state = 0
            self.isNTHovered = False


        if self.ST_button_rect.collidepoint(pg.mouse.get_pos()):
            self.ST_button_state = 1
            if not self.isSTHovered:
                button_hover_sound.play()
                self.isSTHovered = True
                
            if pg.mouse.get_just_pressed()[0]:
                button_click_sound.play()
                self.ST_button_state = 2
                if game.gold_quantity >= Tower_upgrades[f'level{self.tower_level['ST']}']['cost'] and self.tower_level['ST'] < 3:
                    game.gold_quantity -= Tower_upgrades[f'level{self.tower_level['ST']}']['cost']
                    self.tower_level['ST'] += 1
                    outer_archers[0].attack_range = Tower_upgrades[f'level{self.tower_level['ST']}']['range']
                    outer_archers[0].damage = Tower_upgrades[f'level{self.tower_level['ST']}']['dmg']
                    outer_archers[0].animation_speed = Tower_upgrades[f'level{self.tower_level['ST']}']['fire_rate']


        else :
            self.ST_button_state = 0
            self.isSTHovered = False


        if self.ET_button_rect.collidepoint(pg.mouse.get_pos()):
            self.ET_button_state = 1
            if not self.isETHovered:
                button_hover_sound.play()
                self.isETHovered = True

            if pg.mouse.get_just_pressed()[0]:
                button_click_sound.play()
                self.ET_button_state = 2
                if game.gold_quantity >= Tower_upgrades[f'level{self.tower_level['ET']}']['cost'] and self.tower_level['ET'] < 3:
                    game.gold_quantity -= Tower_upgrades[f'level{self.tower_level['ET']}']['cost']
                    self.tower_level['ET'] += 1
                    outer_archers[3].attack_range = Tower_upgrades[f'level{self.tower_level['ET']}']['range']
                    outer_archers[3].damage = Tower_upgrades[f'level{self.tower_level['ET']}']['dmg']
                    outer_archers[3].animation_speed = Tower_upgrades[f'level{self.tower_level['ET']}']['fire_rate']

        else :
            self.ET_button_state = 0
            self.isETHovered = False


        if self.WT_button_rect.collidepoint(pg.mouse.get_pos()):
            self.WT_button_state = 1
            if not self.isWTHovered:
                button_hover_sound.play()
                self.isWTHovered = True
                
            if pg.mouse.get_just_pressed()[0]:
                button_click_sound.play()
                self.WT_button_state = 2
                if game.gold_quantity >= Tower_upgrades[f'level{self.tower_level['WT']}']['cost'] and self.tower_level['WT'] < 3:
                    game.gold_quantity -= Tower_upgrades[f'level{self.tower_level['WT']}']['cost']
                    self.tower_level['WT'] += 1
                    outer_archers[1].attack_range = Tower_upgrades[f'level{self.tower_level['WT']}']['range']
                    outer_archers[1].damage = Tower_upgrades[f'level{self.tower_level['WT']}']['dmg']
                    outer_archers[1].animation_speed = Tower_upgrades[f'level{self.tower_level['WT']}']['fire_rate']
                    
        else :
            self.WT_button_state = 0
            self.isWTHovered = False
