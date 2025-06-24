import pygame, os, json

from GameObject import *
from Setting import *

# check_collide problem!
class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("StarBeat!")
        self.clock = pygame.time.Clock()
        self.init_music()
        self.init_score()
        self.init_sprites()
        self.init_menu()
        # pygame.display.update()
        self.quit_directly = False
        self.pause = False
        self.running = False
        self.creating = False
    
    def init_menu(self):
        self.menu = Menu()
        self.all_sprites.add(self.menu)
        pygame.display.update()
  

    def init_sprites(self):
        self.screen.fill(BLACK)
        self.all_sprites = pygame.sprite.Group()
        self.notes = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.colliders = pygame.sprite.Group()

        self.notes_holder = NotesHolder()

        self.collider_d = Collider(BUTTON_D_POS_X, 'd')
        self.colliders.add(self.collider_d)
        self.collider_f = Collider(BUTTON_D_POS_X + BUTTON_SPACE, 'f')
        self.colliders.add(self.collider_f)
        self.collider_j = Collider(BUTTON_D_POS_X + BUTTON_SPACE * 2, 'j')
        self.colliders.add(self.collider_j)
        self.collider_k = Collider(BUTTON_D_POS_X + BUTTON_SPACE * 3, 'k')
        self.colliders.add(self.collider_k)

        self.button_d = Button(BUTTON_D_POS_X)
        self.buttons.add(self.button_d)
        self.button_f = Button(BUTTON_D_POS_X + BUTTON_SPACE)
        self.buttons.add(self.button_f)
        self.button_j = Button(BUTTON_D_POS_X + BUTTON_SPACE * 2)
        self.buttons.add(self.button_j)
        self.button_k = Button(BUTTON_D_POS_X + BUTTON_SPACE * 3)
        self.buttons.add(self.button_k)

        self.all_sprites.add(self.notes_holder)
        self.all_sprites.add(self.notes)
        self.all_sprites.add(self.buttons)
        self.all_sprites.add(self.colliders)

        pygame.display.update()

    def init_music(self):
        pygame.mixer.music.load(os.path.join("music", MUSIC))
        pygame.mixer.music.set_volume(VOLUME)

    def init_score(self):
        self.pure = 0
        self.far = 0
        self.lost = 0

    def start(self):
        # self.__init__()
        self.wait = True
        while self.wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.wait = False

                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_SPACE]:
                    self.load_map()
                    self.init_score()
                    self.running = True
                    self.wait = False
                    self.run()

                if key_pressed[pygame.K_TAB]:
                    self.creating = True
                    self.wait = False
                    self.create_map()

    def run(self):
        pygame.mixer.music.play()
        while self.running:
            self.clock.tick(FPS)
            self.event_handle()
            # self.check_collide()
            # self.new_check_collide()
            self.check_holding()
            self.check_lost_note()
            self.update_sprite()
            pygame.display.update()
        self.run_finished()

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_directly = True
                self.creating = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause = not self.pause
                    self.pause_running()
                    self.running = True # why need to plus this code?
                    # print(self.running)
                if event.key == pygame.K_q:
                    pygame.mixer.music.stop()
                    self.pause = False
                    self.creating = False
                    self.running = False
                    self.wait = True

                if event.key == pygame.K_d and not self.button_d.set_timer:
                    # print(self.notes_holder.rect.y)
                    self.button_d.active = True
                    self.button_d.pressed = True
                    self.new_check_collide('d')
                if event.key == pygame.K_f and not self.button_f.set_timer:
                    # print(self.notes_holder.rect.y)
                    self.button_f.active = True
                    self.button_f.pressed = True
                    self.new_check_collide('f')
                if event.key == pygame.K_j and not self.button_j.set_timer:
                    # print(self.notes_holder.rect.y)
                    self.button_j.active = True
                    self.button_j.pressed = True
                    self.new_check_collide('j')
                if event.key == pygame.K_k and not self.button_k.set_timer:
                    # print(self.notes_holder.rect.y)
                    self.button_k.active = True
                    self.button_k.pressed = True
                    self.new_check_collide('k')

                if self.creating:
                    if event.key == pygame.K_x and not self.button_d.hold_creating:
                        self.button_d.active = True
                        self.button_d.start_create_hold = True
                        self.button_d.hold_creating = True
                    if event.key == pygame.K_c and not self.button_f.hold_creating:
                        self.button_f.active = True
                        self.button_f.start_create_hold = True
                        self.button_f.hold_creating = True
                    if event.key == pygame.K_m and not self.button_j.hold_creating:
                        self.button_j.active = True
                        self.button_j.start_create_hold = True
                        self.button_j.hold_creating = True
                    if event.key == pygame.K_COMMA and not self.button_k.hold_creating:
                        self.button_k.active = True
                        self.button_k.start_create_hold = True
                        self.button_k.hold_creating = True

            
            if  event.type == pygame.KEYUP:
                if self.running:
                    if event.key == pygame.K_d:
                        self.button_d.pressed = False
                        self.new_check_collide('d', True)
                    if event.key == pygame.K_f:
                        self.button_f.pressed = False
                        self.new_check_collide('f', True)
                    if event.key == pygame.K_j:
                        self.button_j.pressed = False
                        self.new_check_collide('j', True)
                    if event.key == pygame.K_k:
                        self.button_k.pressed = False
                        self.new_check_collide('k', True)

                if self.creating:
                    if event.key == pygame.K_x:
                        self.button_d.active = False
                        self.button_d.end_create_hold = True
                        self.button_d.hold_creating = False
                    if event.key == pygame.K_c:
                        self.button_f.active = False
                        self.button_f.end_create_hold = True
                        self.button_f.hold_creating = False
                    if event.key == pygame.K_m:
                        self.button_j.active = False
                        self.button_j.end_create_hold = True
                        self.button_j.hold_creating = False
                    if event.key == pygame.K_COMMA:
                        self.button_k.active = False
                        self.button_k.end_create_hold = True
                        self.button_k.hold_creating = False

        if not pygame.mixer.music.get_busy():
            self.running = False
            self.creating = False

    def check_collide(self):
        notes_pass = pygame.sprite.groupcollide(self.notes, self.colliders, False, False)
        for note in notes_pass:
            # differ = abs(note.rect.centery - BUTTON_D_POS_Y)
            buttons_dict = {'d':self.button_d, 'f':self.button_f, 'j':self.button_j, 'k':self.button_k}
            # if buttons_dict[notes_pass[note][0].name].active:
            #     if differ <= 20 / fallspeed:
            #         if not note.pressed:
            #             print("PURE")
            #             self.pure += 1
            #             note.pressed = True
            #     elif differ <= 40 / fallspeed:
            #         if not note.pressed:
            #             print("FAR")
            #             self.far += 1
            #             note.pressed = True
            #     else:
            #         if not note.pressed:
            #             note.pressed = True
            #             note.lost = True
            #             print("LOST")
            #             self.lost += 1
            #    note.kill()
            self.check_pressed_timing(note, notes_pass[note][0])
            # if note.rect.top > buttons_dict[notes_pass[note][0].name].rect.bottom and not note.lost and not note.pressed:
            if note.rect.top > buttons_dict[notes_pass[note][0].name].rect.bottom and not note.lost and not note.pressed:
                # if buttons_dict[notes_pass[note][0].name].active:
                self.check_pressed_timing(note, notes_pass[note][0], late = True)
                # note.lost = True
                # print("LOST")
                # self.lost += 1
                # note.kill()
            elif not note.lost and not note.pressed:
                # self.check_pressed_timing(note, notes_pass[note][0], late = True)
                note.lost = True
                # print("LOST")
                self.lost += 1
                # note.kill()

    def new_check_collide(self, collider_name, keyup = False):
        collider_dict = {'d':self.collider_d, 'f':self.collider_f, 'j':self.collider_j, 'k':self.collider_k}
        notes_pass = pygame.sprite.spritecollide(collider_dict[collider_name], self.notes, False, None)
        # print(notes_pass)
        for note in notes_pass:
            print(note)
            if note.type == "Tap":
                self.check_pressed_timing(note, collider_dict[collider_name])
                break # very important
            elif note.type == "Hold":
                self.check_pressed_timing(note, collider_dict[collider_name])
                self.check_press_hold(note, collider_dict[collider_name])
                break
            
            if keyup:
                # self.check_keyup_timing(note, collider_dict[collider_name])
                self.check_press_hold(note, collider_dict[collider_name]) # important
        
    def check_lost_note(self):
        notes_pass = pygame.sprite.groupcollide(self.notes, self.colliders, False, False)
        for note in notes_pass:
            if note.type == "Tap":
                if note.rect.top > SCREEN_HEIGHT:
                    note.lost = True
                    self.lost += 1
                    note.kill()
            if note.type == "Hold":
                if not note.pressed:
                    if note.rect.bottom > SCREEN_HEIGHT:
                        self.lost += note.check_times
                        note.kill()
                # if note.pressed:
                #     if note.rect.top > SCREEN_HEIGHT:
                #         self.lost += 1
                #         note.kill()

    def check_pressed_timing(self, note, collider, late = False):
        # differ = abs(self.notes_holder.rect.y - note.STDy)
        if note.type == "Tap":
            differ = abs(collider.rect.centery - note.rect.centery)
            buttons_dict = {'d':self.button_d, 'f':self.button_f, 'j':self.button_j, 'k':self.button_k}
            if buttons_dict[collider.name].active and not note.pressed:
                # print(differ)
                if differ <= COLLIDER_SIZE[1] * 0.2:
                    # if not note.pressed:
                        # print("PURE")
                        self.pure += 1
                        note.pressed = True
                elif differ <= COLLIDER_SIZE[1] * 0.5:
                    # if not note.pressed:
                        # print("FAR")
                        self.far += 1
                        note.pressed = True
                else:
                    # if not note.pressed:
                        note.pressed = True
                        note.lost = True
                        # print("LOST")
                        self.lost += 1
                note.kill()

        # if late and not note.pressed:
        #     print("late!" + str(differ))
        #     # if differ <= 10:
        #     #     if not note.pressed:
        #     #         # print("PURE")
        #     #         self.pure += 1
        #     #         note.pressed = True
        #     if differ <= COLLIDER_SIZE[1] - 20:
        #         # if not note.pressed:
        #             # print("FAR")
        #             self.far += 1
        #             note.pressed = True
        #     else:
        #         # if not note.pressed:
        #             note.pressed = True
        #             note.lost = True
        #             # print("LOST")
        #             self.lost += 1

        # if late:
        #     note.pressed = True
        #     note.lost = True
        #     self.lost += 1

        if note.type == "Hold":
            start_differ = abs(collider.rect.centery - note.rect.bottom)
            # buttons_dict = {'d':self.button_d, 'f':self.button_f, 'j':self.button_j, 'k':self.button_k}
            # if buttons_dict[collider.name].active and not note.pressed:
            if not note.pressed:
                if start_differ <= COLLIDER_SIZE[1] * 0.2:
                    self.pure += 1
                    note.pressed = True
                elif start_differ <= COLLIDER_SIZE[1] * 0.5:
                    self.far += 1
                    note.pressed = True
                elif start_differ > COLLIDER_SIZE[1] * 0.5:
                    self.lost += 1
                    note.pressed = True
                note.check_times -= 1
    
    def check_press_hold(self, note, collider):
        # print("Check"+str(note))
        buttons_dict = {'d':self.button_d, 'f':self.button_f, 'j':self.button_j, 'k':self.button_k}
        buttons_dict[collider.name].hold_checking = True
        if note.check_times >= 1:
            if not buttons_dict[collider.name].pressed:
                # print("UP")
                self.lost += note.check_times
                note.check_times = 0 # in case to make additional lost
                note.kill()
            else:
                self.pure += 1
                note.check_times -= 1
        if note.check_times == 0:
            buttons_dict[collider.name].hold_checking = False

    def check_holding(self):
        if self.button_d.hold_checking:
            self.new_check_collide('d')
        if self.button_f.hold_checking:
            self.new_check_collide('f')
        if self.button_j.hold_checking:
            self.new_check_collide('j')
        if self.button_k.hold_checking:
            self.new_check_collide('k')

# need to cancel check keyup and use Hold.check_times to add max_combo
    def check_keyup_timing(self, note, collider):
        end_differ = abs(collider.rect.centery - note.rect.top)
        if note.pressed:
            if end_differ <= COLLIDER_SIZE[1] * 0.2:
                self.pure += 1
            elif end_differ <= COLLIDER_SIZE[1] * 0.5:
                self.far += 1
            elif end_differ > COLLIDER_SIZE[1] * 0.5:
                self.lost += 1
            note.kill()
            
    def update_sprite(self):
        self.screen.fill(BLACK)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)

        # pygame.draw.rect(self.screen, color=WHITE, rect=self.collider_d.rect)
        # print(self.button_d.set_timer)
        
    def run_finished(self):
        if not self.quit_directly:
            self.wait = True
            self.running = False
            self.show_score() # temporary
            self.init_sprites()
            self.start()
        else:
            self.show_score() # temporary
            pygame.quit()

    def load_map(self):
        note_x = {'d':BUTTON_D_POS_X, 'f':BUTTON_D_POS_X+BUTTON_SPACE, 'j':BUTTON_D_POS_X+BUTTON_SPACE*2, 'k':BUTTON_D_POS_X+BUTTON_SPACE*3}
        with open(os.path.join("map", MAP), 'r') as file:
            data = json.load(file)
            for i in range(data["NOTE_NUM"]):
                if data["NOTES"][i][0] == "Tap":
                    note = Tap(note_x[data["NOTES"][i][1]], data["NOTES"][i][2])
                    self.notes.add(note)
                elif data["NOTES"][i][0] == "Hold":
                    note = Hold(note_x[data["NOTES"][i][1]], data["NOTES"][i][2], data["NOTES"][i][3])
                    self.notes.add(note)

            self.all_sprites.add(self.notes)

    def create_map(self):
        pygame.mixer.music.play()
        self.note_num = 0
        self.max_combo = 0
        self.record_data = [[]*2 for i in range(0)]
        while self.creating:
            self.clock.tick(FPS)
            self.event_handle()
            self.record_key()
            self.update_sprite()
            pygame.display.update()
        self.record_map()
        self.run_finished()

    def record_key(self):
        if self.button_d.active and not self.button_d.set_timer and not self.button_d.hold_creating:
            self.record_data.append(["Tap", "d", self.notes_holder.rect.y])
            self.note_num += 1
            self.max_combo += 1
             
        if self.button_f.active and not self.button_f.set_timer and not self.button_f.hold_creating:
            self.record_data.append(["Tap", "f", self.notes_holder.rect.y])
            self.note_num += 1
            self.max_combo += 1
        
        if self.button_j.active and not self.button_j.set_timer and not self.button_j.hold_creating:
            self.record_data.append(["Tap", "j", self.notes_holder.rect.y])
            self.note_num += 1
            self.max_combo += 1
            
        if self.button_k.active and not self.button_k.set_timer and not self.button_k.hold_creating:
            self.record_data.append(["Tap", "k", self.notes_holder.rect.y])
            self.note_num += 1
            self.max_combo += 1


        if self.button_d.start_create_hold:
            self.button_d.hold_start = self.notes_holder.rect.y
            self.button_d.start_create_hold = False
        if self.button_d.end_create_hold:
            self.button_d.hold_end = self.notes_holder.rect.y 
            self.record_data.append(["Hold", "d", self.button_d.hold_start, self.button_d.hold_end])
            self.note_num += 1
            self.button_d.hold_check_times = int((self.button_d.hold_end - self.button_d.hold_start) // NOTE_SIZE[1])
            if self.button_d.hold_check_times < 1:
                self.button_d.hold_check_times = 1
            self.max_combo += self.button_d.hold_check_times
            self.button_d.end_create_hold = False
                
        if self.button_f.start_create_hold:
            self.button_f.hold_start = self.notes_holder.rect.y
            self.button_f.start_create_hold = False
        if self.button_f.end_create_hold:
            self.button_f.hold_end = self.notes_holder.rect.y 
            self.record_data.append(["Hold", "f", self.button_f.hold_start, self.button_f.hold_end])
            self.note_num += 1
            self.button_f.hold_check_times = int((self.button_f.hold_end - self.button_f.hold_start) // NOTE_SIZE[1])
            if self.button_f.hold_check_times < 1:
                self.button_f.hold_check_times = 1
            self.max_combo += self.button_f.hold_check_times
            self.button_f.end_create_hold = False

        if self.button_j.start_create_hold:
            self.button_j.hold_start = self.notes_holder.rect.y
            self.button_j.start_create_hold = False
        if self.button_j.end_create_hold:
            self.button_j.hold_end = self.notes_holder.rect.y 
            self.record_data.append(["Hold", "j", self.button_j.hold_start, self.button_j.hold_end])
            self.note_num += 1
            self.button_j.hold_check_times = int((self.button_j.hold_end - self.button_j.hold_start) // NOTE_SIZE[1])
            if self.button_j.hold_check_times < 1:
                self.button_j.hold_check_times = 1
            self.max_combo += self.button_j.hold_check_times
            self.button_j.end_create_hold = False

        if self.button_k.start_create_hold:
            self.button_k.hold_start = self.notes_holder.rect.y
            self.button_k.start_create_hold = False
        if self.button_k.end_create_hold:
            self.button_k.hold_end = self.notes_holder.rect.y 
            self.record_data.append(["Hold", "k", self.button_k.hold_start, self.button_k.hold_end])
            self.note_num += 1
            self.button_k.hold_check_times = int((self.button_k.hold_end - self.button_k.hold_start) // NOTE_SIZE[1])
            if self.button_k.hold_check_times < 1:
                self.button_k.hold_check_times = 1
            print(self.button_k.hold_check_times)
            self.max_combo += self.button_k.hold_check_times
            self.button_k.end_create_hold = False
          
    def record_map(self):
        data = {"NOTE_NUM":self.note_num, "MAX_COMCO":self.max_combo, "NOTES":self.record_data}
        with open(os.path.join("map", MAP), 'w') as file:
            json.dump(data, file)
            print("recorded!")

# something wrong
    def pause_running(self):
        pygame.mixer.music.pause()
        # print(self.pause)
        while self.pause:
            self.clock.tick(FPS)
            self.event_handle()
            if self.quit_directly:
                self.pause = False
                self.run_finished()
        if not self.pause:
            pygame.mixer.music.unpause()

    def show_score(self):
        print("PURE:", self.pure)
        print("FAR:", self.far)
        print("LOST", self.lost)

if __name__ == "__main__":
    game = Game()
    game.start()