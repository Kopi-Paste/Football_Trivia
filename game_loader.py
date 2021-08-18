import pygame
import os
import csv


windowWidth = 1280
windowHeight = 1040
standardButtonWidth = 361
standardButtonHeight = 114

mainMenuButtonsDir = "assets/Menu_buttons/"
iconFile = "assets/football.png"
emptyButtonFile = "assets/emptyButton.png"
confirmButtonFile = "assets/confirmButton.png"
cancelButtonFile = "assets/cancelButton.png"
questionsFile = "questions.csv"
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
        self.clickedOn = False
        self.cursorPosition = 0
        try:
            self.font = pygame.font.Font(fontFile, 25)
        except:
            self.font = pygame.font.Font(None, 25)
        self.userInput = ""

    def BlitOnScreen(self, display):
        super(UserInputButton, self).BlitOnScreen(display)
        textParts = list()
        for i in range((len(self.userInput) // 35) + 1):
            textParts.append(self.userInput[i * 35:((i + 1) * 35)])
        for i in range(len(textParts)):
            if i != len(textParts) - 1:
                while not textParts[i].endswith(' '):
                    textParts[i + 1] = textParts[i][-1] + textParts[i + 1]
                    textParts[i] = textParts[i][:-1]

            text = self.font.render(textParts[i], True, (0, 0, 0), (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (self.XAxis + self.width / 2, self.YAxis + 20 + i * 25)
            display.blit(text, textRect)

    def ShowCursor(self, replaceMode = 0):
        self.userInput = self.userInput.replace("|", "")
        if replaceMode == 0:
            self.userInput = self.userInput[:self.cursorPosition] + '|' + self.userInput[self.cursorPosition:]
        elif replaceMode == 1:
            self.userInput = self.userInput[:self.cursorPosition - 1] + '|' + self.userInput[self.cursorPosition:]
        elif replaceMode == 2:
            self.userInput = self.userInput[:self.cursorPosition] + '|' + self.userInput[self.cursorPosition + 1:]

    def HideCursor(self):
            self.userInput = self.userInput.replace('|', "")

    def AddChar(self, key):
        if (len(self.userInput)) == 160 or key == "|":
            return
        oldString = self.userInput
        self.userInput = self.userInput.replace("|", key)
        self.cursorPosition += len(self.userInput) - len(oldString) + 1
        self.ShowCursor()


    def RemovePrevious(self):
        if self.cursorPosition == 0:
            return
        self.ShowCursor(1)
        self.MoveCursorLeft()


    def RemoveNext(self):
        if self.cursorPosition == len(self.userInput) - 1:
            return
        self.ShowCursor(2)

    def MoveCursorLeft(self, max = False):
        if (max or self.cursorPosition == 0):
            self.cursorPosition = 0
        else:
            self.cursorPosition -= 1
        self.ShowCursor()

    def MoveCursorRight(self, max = False):
        if (max or self.cursorPosition == len(self.userInput) - 1):
            self.cursorPosition = len(self.userInput) - 1
        else:
            self.cursorPosition += 1
        self.ShowCursor()

class Question:
    def __init__(self, question, correctAnswer, badAnswers):
        self.question = question
        self.correctAnswer = correctAnswer
        self.badAnswers = badAnswers
    def WriteToCSV(self):
        with open(questionsFile, mode='a', newline='', encoding='utf-8') as questions:
            questionWriter = csv.writer(questions, delimiter=';')
            questionWriter.writerow([self.question, self.correctAnswer, self.badAnswers[0], self.badAnswers[1], self.badAnswers[2]])

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
    for i in range(5):
        try:
            buttonList.append(UserInputButton(emptyButtonFile, coordinates[i][0], coordinates[i][1], standardButtonWidth, standardButtonHeight))
        except:
           pygame.quit()
           exit("Not found file " + emptyButtonFile)
    buttonList.append(Button(cancelButtonFile, 100, 800, standardButtonWidth, standardButtonHeight))
    buttonList.append(Button(confirmButtonFile, windowWidth - 100 - standardButtonWidth, 800, standardButtonWidth, standardButtonHeight))
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

