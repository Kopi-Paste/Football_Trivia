import pygame
import os


windowWidth = 1280
windowHeight = 1040
mainMenuButtonWidth = 361
mainMenuButtonHeight = 114

mainMenuButtonsDir = "assets/Menu_buttons/"
iconFile = "assets/football.png"


class Screen:
    def __init__(self, screenDisplay, background, buttons):
        self.display = screenDisplay
        self.background = background
        self.buttons = buttons

    def Draw(self):
        self.display.fill(self.background)
        for button in self.buttons:
            button.BlitOnScreen(self.display)


class Button:
    def __init__(self, file, x_axis, y_axis, width, height):
        self.file = pygame.image.load(file)
        self.XAxis = x_axis
        self.YAxis = y_axis
        self.width = width
        self.height = height

    def BlitOnScreen(self, display):
        display.blit(self.file, (self.XAxis, self.YAxis))

    def MouseCollision(self, mousePosition):
        return self.XAxis <= mousePosition[0] <= (self.XAxis + self.width) and self.YAxis <= mousePosition[1] <= (self.YAxis + self.height)


def GeneralSetup():
    pygame.display.set_caption("Football Trivia")
    try:
        icon = pygame.image.load(iconFile)
    except:
        pygame.quit()
        exit("Not found file " + iconFile)
    pygame.display.set_icon(icon)
    FirstScreenSetup()

def MainMenuButtonsLoader():
    buttonList = list();
    i = 0
    for file in os.listdir(mainMenuButtonsDir):
        try:
            buttonList.append(Button(mainMenuButtonsDir + file, (windowWidth - 361) / 2, 200 + (i * 200), mainMenuButtonWidth, mainMenuButtonHeight))
        except:
            pygame.quit()
            exit("Not found directory: " + mainMenuButtonsDir)
        i += 1
    return buttonList

def FirstScreenSetup():
    import current_display
    firstScreenDisplay = pygame.display.set_mode((windowWidth, windowHeight))
    firstScreen = Screen(firstScreenDisplay, (71, 174, 56), MainMenuButtonsLoader())
    current_display.currentScreen = firstScreen
    current_display.currentButtons = firstScreen.buttons

""" import easygui
Soubory:
file = easygui.fileopenbox()
Složky:
dir = easygui.diropenbox();
"""


