import pygame

import game_loader


def GameLoop(state):
    if state == 0: # První obrazovka
        return MainMenuLoop()
    elif state == 4:
        return AddQuestionLoop()



def MainMenuLoop():
    import current_display
    current_display.DisplayScreen()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return -1
        elif event.type == pygame.MOUSEBUTTONUP:
            clickedButtonNumber = current_display.DetermineClickedButton(pygame.mouse.get_pos())
            if clickedButtonNumber == 0:
                pass
            elif clickedButtonNumber == 1:
                game_loader.AddQuestionScreenSetup()
                return 4
            elif clickedButtonNumber == 2:
                pass
            elif clickedButtonNumber == 3:
                return -1
    return 0

def PlayGameLoop():
    pass

def WinGameLoop():
    pass

def LossGameLoop():
    pass

def AddQuestionLoop():
    import current_display
    current_display.DisplayScreen()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return -1
    return 4

def ImportExportLoop():
    pass

