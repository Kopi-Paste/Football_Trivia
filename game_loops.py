import pygame


def GameLoop(state):
    import current_display
    if state == 0: # První obrazovka
        current_display.DisplayScreen()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.MOUSEBUTTONUP:
                clickedButtonNumber = current_display.DetermineClickedButton(pygame.mouse.get_pos())
                if (clickedButtonNumber == 0):
                    
        return 0

