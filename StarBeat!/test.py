import pygame, os
import subprocess

screen = pygame.display.set_mode((300, 300))
# print((1.5)/4)
pygame.init()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        # if event.type == pygame.KEYDOWN:
        #     print(pygame.K_LESS)
        #     print("DOWN")
        # if event.type == pygame.KEYUP:
        #     print("UP")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("LeftClick")
            if event.button == 2:
                print("CenterClick")
                FILE_PATH = os.path.join("C:", "path", "of", "folder", "file")
                user_import = subprocess.Popen(fr'explorer /select,{FILE_PATH}')
                user_music = user_import.communicate()
                print(user_music)
            if event.button == 3:
                print("RightClick")
            if event.button == 4:
                print("RollUp")
            if event.button == 5:
                print("RollDown")
            