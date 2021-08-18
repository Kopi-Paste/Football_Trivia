import pygame

import game_loader


def GameLoop(state):
    if state == 0: # První obrazovka
        return MainMenuLoop()
    elif state == 1:
        return PlayGameLoop()
    elif state == 2:
        return WinGameLoop()
    elif state == 3:
        return LossGameLoop()
    elif state == 4:
        return AddQuestionLoop()
    elif state == 5:
        return BestScoresLoop()



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
                game_loader.GameScreenSetup()
                return 1

            elif clickedButtonNumber == 1:
                game_loader.AddQuestionScreenSetup()
                return 4
            elif clickedButtonNumber == 2:
                pass
            elif clickedButtonNumber == 3:
                return -1
    return 0

def PlayGameLoop():
    import current_display
    current_display.DisplayScreen()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return -1
        elif event.type == pygame.MOUSEBUTTONUP:
            clickedButtonNumber = current_display.DetermineClickedButton(pygame.mouse.get_pos())
            if clickedButtonNumber == current_display.currentQuestions[current_display.currentQuestion].correctAnswerIndex:
                if current_display.currentQuestion != 14:
                    current_display.currentQuestion += 1
                    newQuestionButtons = current_display.currentQuestions[current_display.currentQuestion].ToButtons()
                    current_display.currentScreen.buttons = newQuestionButtons
                    current_display.currentButtons = newQuestionButtons
                    return 1
                else:
                    return 0  #Výhra
            elif clickedButtonNumber != 0 and clickedButtonNumber != -1:
                game_loader.FirstScreenSetup() #Prohra
                return 0
    return 1

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

def BestScoresLoop():
    pass

