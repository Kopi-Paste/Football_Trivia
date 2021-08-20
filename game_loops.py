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
                game_loader.HighscoresScreenSetup()
                return 5
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
                    current_display.currentScreen.HideArrow(current_display.currentQuestion)
                    current_display.currentQuestion += 1
                    newQuestionButtons = current_display.currentQuestions[current_display.currentQuestion].ToButtons()
                    current_display.currentScreen.buttons = newQuestionButtons
                    current_display.currentButtons = newQuestionButtons
                    current_display.currentScreen.ShowArrow(current_display.currentQuestion)
                    return 1
                else:
                    current_display.score = game_loader.scores[-1]
                    game_loader.WinGameScreenSetup()
                    return 3  #Výhra
            elif clickedButtonNumber == 5:
                current_display.score = game_loader.scores[current_display.currentQuestion]
                game_loader.LossGameScreenSetup(current_display.currentQuestions[current_display.currentQuestion].correctAnswer, current_display.score)
                return 3
            elif clickedButtonNumber != 0 and clickedButtonNumber != -1:
                current_display.score = game_loader.scores[current_display.currentQuestion - current_display.currentQuestion % 5]
                game_loader.LossGameScreenSetup(current_display.currentQuestions[current_display.currentQuestion].correctAnswer, current_display.score) #Prohra
                return 3
    return 1

def WinGameLoop():
    import current_display

def LossGameLoop():
    import current_display
    current_display.DisplayScreen()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return -1
        elif event.type == pygame.MOUSEBUTTONUP:
            clickedButtonNumber = current_display.DetermineClickedButton(pygame.mouse.get_pos())
            if clickedButtonNumber == 0:
                current_display.currentButtons[0].clickedOn = True
                current_display.currentButtons[0].ShowCursor()
            elif clickedButtonNumber == 1:
                current_display.currentButtons[0].clickedOn = False
                current_display.currentButtons[0].HideCursor()
                game_loader.FirstScreenSetup()
                return 0
            elif clickedButtonNumber == 2:
                current_display.currentButtons[0].clickedOn = False
                current_display.currentButtons[0].HideCursor()
                if current_display.currentButtons[0].text == "":
                    return 3
                game_loader.WriteScore(current_display.currentButtons[0].text, current_display.score)
                game_loader.HighscoresScreenSetup()
                return 5
            elif clickedButtonNumber == -1:
                current_display.currentButtons[0].clickedOn = False
                current_display.currentButtons[0].HideCursor()
        elif event.type == pygame.KEYDOWN:
            if current_display.currentButtons[0].clickedOn:
                if event.key == pygame.K_BACKSPACE:
                    current_display.currentButtons[0].RemovePrevious()
                elif event.key == pygame.K_DELETE:
                    current_display.currentButtons[0].RemoveNext()
                elif event.key == pygame.K_LEFT:
                    current_display.currentButtons[0].MoveCursorLeft()
                elif event.key == pygame.K_RIGHT:
                    current_display.currentButtons[0].MoveCursorRight()
                elif event.key == pygame.K_HOME:
                    current_display.currentButtons[0].MoveCursorLeft(True)
                elif event.key == pygame.K_END:
                    current_display.currentButtons[0].MoveCursorRight(True)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    current_display.currentButtons[0].HideCursor()
                else:
                    current_display.currentButtons[0].AddChar(event.unicode)
    return 3

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
                        if current_display.currentButtons[i].textGraphic == "":
                            return 4
                    game_loader.Question(current_display.currentButtons[0].textGraphic, current_display.currentButtons[1].textGraphic, (current_display.currentButtons[2].textGraphic, current_display.currentButtons[3].textGraphic, current_display.currentButtons[4].textGraphic)).WriteToCSV()
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
    import current_display
    current_display.DisplayScreen()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return -1
        elif event.type == pygame.MOUSEBUTTONUP:
            game_loader.FirstScreenSetup()
            return 0
    return 5