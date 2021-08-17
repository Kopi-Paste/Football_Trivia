import pygame
import os


windowWidth = 1280
windowHeight = 1040
standardButtonWidth = 361
standardButtonHeight = 114

mainMenuButtonsDir = "assets/Menu_buttons/"
iconFile = "assets/football.png"
emptyButtonFile = "assets/emptyButton.png"
fontFile = "assets/cappungFont.otf"  # by 7NTypes ze stránky dafont.com

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

class UserInputButton(Button):
    def __init__(self, file, x_axis, y_axis, width, height):
        super().__init__(file, x_axis, y_axis, width, height)
        self.userInput = ""
        self.clickedOn = False
        try:
            self.font = pygame.font.Font(fontFile, 20)
        except:
            self.font = pygame.font.Font(None, 20)

    def BlitOnScreen(self, display):
        text = self.font.render(self.userInput, True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = ((self.XAxis + self.width) / 2, (self.YAxis + self.height) / 2)
        display.blit(text, textRect)
        super(UserInputButton, self).BlitOnScreen(display)


    def AddChar(self, key):
        char = pygame.key.name(key)
        self.userInput += char.decode('unicode_escape')




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
            buttonList.append(Button(mainMenuButtonsDir + file, (windowWidth - standardButtonWidth) / 2, 200 + (i * 200), standardButtonWidth, standardButtonHeight))
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

def AddQuestionButtonsLoader():
    buttonList = list()
    coordinates = [((windowWidth - standardButtonWidth) / 2, 200), (200, 400), (windowWidth - 200 - standardButtonWidth, 400), (200, 600), (windowWidth - 200 - standardButtonWidth, 600)]
    for i in range(0, 5):
        try:
            buttonList.append(UserInputButton(emptyButtonFile, coordinates[i][0], coordinates[i][1], standardButtonWidth, standardButtonHeight))
        except:
            pygame.quit()
            exit("Not found file " + emptyButtonFile)
    return buttonList

def AddQuestionScreenSetup():
    import current_display
    addQuestionScreenDisplay = pygame.display.set_mode((windowWidth, windowHeight))
    addQuestionScreen = Screen(addQuestionScreenDisplay, (71, 174, 56), AddQuestionButtonsLoader())
    current_display.currentScreen = addQuestionScreen
    current_display.currentButtons = addQuestionScreen.buttons

""" import easygui
Soubory:
file = easygui.fileopenbox()
Složky:
dir = easygui.diropenbox();
"""


