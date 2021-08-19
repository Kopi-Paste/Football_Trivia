import pygame

currentScreen = None

currentButtons = None

currentQuestions = None

currentQuestion = 0

score = 0


def DisplayScreen():
    currentScreen.Draw()

def DetermineClickedButton(mousePosition):
    i = 0
    for button in currentButtons:
        if button.MouseCollision(mousePosition):
            return i
        i += 1
    return -1

