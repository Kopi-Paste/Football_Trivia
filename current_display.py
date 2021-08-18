import pygame

currentScreen = None

currentButtons = None


def DisplayScreen():
    currentScreen.Draw()

def DetermineClickedButton(mousePosition):
    i = 0
    for button in currentButtons:
        if button.MouseCollision(mousePosition):
            return i
        i += 1
