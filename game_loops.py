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
        elif event.type == pygame.MOUSEBUTTONUP:
            clickedButtonNumber = current_display.DetermineClickedButton(pygame.mouse.get_pos())
            for i in range(len(current_display.currentButtons)):
                if i == clickedButtonNumber and i < 5:
                    current_display.currentButtons[i].clickedOn = True
                    current_display.currentButtons[i].ShowCursor()
                elif i < 5:
                    current_display.currentButtons[i].clickedOn = False
                    current_display.currentButtons[i].HideCursor()
                elif clickedButtonNumber == 5:
                    game_loader.FirstScreenSetup()
                    return 0
                elif clickedButtonNumber == 6:
                    for i in range(5):
                        if current_display.currentButtons[i].text == "":
                            return 4
                    game_loader.Question(current_display.currentButtons[0].text, current_display.currentButtons[1].text, (current_display.currentButtons[2].text, current_display.currentButtons[3].text, current_display.currentButtons[4].text)).WriteToCSV()
                    game_loader.FirstScreenSetup()
                    return 0

        elif event.type == pygame.KEYDOWN:
            for button in current_display.currentButtons:
                if isinstance(button, game_loader.ButtonWithText) and button.clickedOn:
                    if event.key == pygame.K_BACKSPACE:
                        button.RemovePrevious()
                    elif event.key == pygame.K_DELETE:
                        button.RemoveNext()
                    elif event.key == pygame.K_LEFT:
                        button.MoveCursorLeft()
                    elif event.key == pygame.K_RIGHT:
                        button.MoveCursorRight()
                    elif event.key == pygame.K_HOME:
                        button.MoveCursorLeft(True)
                    elif event.key == pygame.K_END:
                        button.MoveCursorRight(True)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        button.HideCursor()
                    else:
                        button.AddChar(event.unicode)



    return 4

def ImportExportLoop():
    pass

