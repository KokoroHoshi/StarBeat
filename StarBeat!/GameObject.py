import pygame, os

from Setting import *

class NotesHolder(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("img", NOTE_HOLDER_IMG))
        self.image = pygame.transform.scale(self.image, NOTEHOLDER_SIZE)
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.centerx = SCREEN_WIDTH // 2
    
    def update(self):
        self.rect.y += FALLSPEED / fallspeed
        # print(self.rect.y)

    
class Tap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join("img", NOTE_IMG))
        self.image = pygame.transform.scale(self.image, NOTE_SIZE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = -y * fallspeed  + OFFSET
        self.STDy = y
        self.pressed = False
        self.lost = False
        self.type = "Tap"
    
    def update(self):
        self.rect.y += FALLSPEED

        # if self.rect.top > SCREEN_HEIGHT:
        #     self.kill()

class Hold(pygame.sprite.Sprite):
    def __init__(self, x, start, end):
        super().__init__()
        self.image = pygame.image.load(os.path.join("img", NOTE_IMG))
        self.long = end - start
        self.check_times = int(self.long // NOTE_SIZE[1])
        if self.check_times <= 1:
            self.check_times = 1
            # like Tap
            self.image = pygame.transform.scale(self.image, (NOTE_SIZE[0], NOTE_SIZE[1] * self.check_times))
        else:
            self.image = pygame.transform.scale(self.image, (NOTE_SIZE[0], NOTE_SIZE[1] * fallspeed * self.check_times))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = -start * fallspeed  + OFFSET
        # self.STDy = y
        # self.pressed = False
        # self.lost = False
        self.type = "Hold"
        self.pressed = False

    
    def update(self):
        self.rect.y += FALLSPEED
        # print(self.check_times)

class Button(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load(os.path.join("img", BUTTON_DEAFULT_IMG))
        self.image = pygame.transform.scale(self.image, BUTTON_SIZE)
        self.image_ori = self.image
        self.image_active = pygame.image.load(os.path.join("img", BUTTON_ACTIVE_IMG))
        self.image_active = pygame.transform.scale(self.image_active, BUTTON_SIZE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = BUTTON_D_POS_Y
        self.active = False
        self.active_start_time = 0
        self.set_timer = False
        self.pressed = False
        self.start_create_hold = False
        self.end_create_hold = False
        self.hold_start = 0
        self.hold_end = 0
        self.hold_creating = False
        self.hold_check_times = 0
        self.hold_checking = False

    def update(self):
        if self.active:
            self.image = self.image_active
            if not self.set_timer:
                self.active_start_time = pygame.time.get_ticks()
                self.set_timer = True
            if pygame.time.get_ticks() - self.active_start_time >= BUTTONS_ACTIVE_TIME:
                self.active = False
                self.set_timer = False
        else:
            self.image = self.image_ori

class Collider(pygame.sprite.Sprite):
    def __init__(self, x, name):
        super().__init__()
        self.image = pygame.image.load(os.path.join("img", NOTE_HOLDER_IMG))
        self.image = pygame.transform.scale(self.image, COLLIDER_SIZE)
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = BUTTON_D_POS_Y
        self.name = name

class UI_text_Button:
    def __init__(self, text, text_rect, size = FONT_SIZE, color = BLACK, BG_color = None):
        self.text = text
        self.rect = text_rect
        self.x = text_rect.x
        self.y = text_rect.y
        self.font_size = size
        self.text_color = color
        self.BG_color = BG_color

    def ChangeTextColor(self, color, surface):
        if color != self.text_color:
            self.text_color = color
            font = pygame.font.Font(os.path.join("font", FONT_MSJH), self.font_size)
            text_surface = font.render(self.text, True, color)
            text_new_rect = text_surface.get_rect()
            text_new_rect.x = self.x
            text_new_rect.y = self.y
            surface.blit(text_surface, text_new_rect)
            pygame.display.update()

class UI_img_button(pygame.sprite.Sprite):
    def __init__(self, ori_img, clicked_img):
        super().__init__()
        
