import pygame
import game_loader
import game_loops

pygame.init()
state = 0

game_loader.GeneralSetup()

while state != -1:
    state = game_loops.GameLoop(state)
else:
    pygame.quit()
    exit()
