import pygame

currentScreen = None

currentButtons = None

currentQuestions = None

currentQuestion = 0

score = 0

fiftyFiftyAvailable = True

friendHelpAvailable = True

publicHelpAvailable = True


def DisplayScreen():
    currentScreen.Draw()

def DetermineClickedButton(mousePosition):
    i = 0
    for button in currentButtons:
        if button is not None and button.MouseCollision(mousePosition):
            return i
        i += 1
    return -1

