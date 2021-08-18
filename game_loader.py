import pygame
import os
import csv
import random

import current_display

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
addQuestionLabelsFile = "labels/addQuestionLabels.csv"
fontFile = "assets/cappung_Font.otf"  # by 7NTypes ze stránky dafont.com

questionButtonCoordinates = [((windowWidth - standardButtonWidth) / 2, 200), (200, 400),
                             (windowWidth - 200 - standardButtonWidth, 400), (200, 600),
                             (windowWidth - 200 - standardButtonWidth, 600)]


class Screen:
    def __init__(self, screenDisplay, background, buttons, labelsList):
        self.display = screenDisplay
        self.background = background
        self.buttons = buttons
        self.labels = labelsList

    def Draw(self):
        self.display.fill(self.background)
        for button in self.buttons:
            button.BlitOnScreen(self.display)
        if self.labels is not None:
            for label in self.labels:
                label.Show(self.display)

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

class ButtonWithText(Button):
    def __init__(self, file, x_axis, y_axis, width, height, text):
        super().__init__(file, x_axis, y_axis, width, height)
        self.clickedOn = False
        self.cursorPosition = 0
        try:
            self.font = pygame.font.Font(fontFile, 25)
        except:
            self.font = pygame.font.Font(None, 25)
        self.text = text

    def BlitOnScreen(self, display):
        super(ButtonWithText, self).BlitOnScreen(display)
        textParts = list()
        for i in range((len(self.text) // 35) + 1):
            if i != 4:
                textParts.append(self.text[i * 35:((i + 1) * 35)])
        for i in range(len(textParts)):
            if i != len(textParts) - 1:
                if " " in textParts[i]:
                    while not (textParts[i].endswith(' ')):
                        textParts[i + 1] = textParts[i][-1] + textParts[i + 1]
                        textParts[i] = textParts[i][:-1]

            text = self.font.render(textParts[i], True, (0, 0, 0), (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (self.XAxis + self.width / 2, self.YAxis + 20 + i * 25)
            display.blit(text, textRect)

    def ShowCursor(self, replaceMode = 0):
        self.text = self.text.replace("|", "")
        if replaceMode == 0:
            self.text = self.text[:self.cursorPosition] + '|' + self.text[self.cursorPosition:]
        elif replaceMode == 1:
            self.text = self.text[:self.cursorPosition - 1] + '|' + self.text[self.cursorPosition:]
        elif replaceMode == 2:
            self.text = self.text[:self.cursorPosition] + '|' + self.text[self.cursorPosition + 1:]

    def HideCursor(self):
            self.text = self.text.replace('|', "")

    def AddChar(self, key):
        if (len(self.text)) == 140 or key == "|":
            return
        oldString = self.text
        self.text = self.text.replace("|", key)
        self.cursorPosition += len(self.text) - len(oldString) + 1
        self.ShowCursor()


    def RemovePrevious(self):
        if self.cursorPosition == 0:
            return
        self.ShowCursor(1)
        self.MoveCursorLeft()


    def RemoveNext(self):
        if self.cursorPosition == len(self.text) - 1:
            return
        self.ShowCursor(2)

    def MoveCursorLeft(self, max = False):
        if (max or self.cursorPosition == 0):
            self.cursorPosition = 0
        else:
            self.cursorPosition -= 1
        self.ShowCursor()

    def MoveCursorRight(self, max = False):
        if max or self.cursorPosition == len(self.text) - 1:
            self.cursorPosition = len(self.text) - 1
        else:
            self.cursorPosition += 1
        self.ShowCursor()

class Label:
    def __init__(self, text, text_size, x_axis, y_axis):
        try:
            self.font = pygame.font.Font(fontFile, text_size)
        except:
            self.font = pygame.font.Font(None, text_size)
        self.text = self.font.render(text, True, (255, 255, 255), (71, 174, 56))
        self.textRect = self.text.get_rect()
        self.textRect.center = (x_axis, y_axis)

    def Show(self, display):
        display.blit(self.text, self.textRect)

class Question:
    def __init__(self, question, correctAnswer, badAnswers):
        self.question = question
        self.correctAnswer = correctAnswer
        self.badAnswers = badAnswers
        self.correctAnswerIndex = 1

    def WriteToCSV(self):
        try:
            with open(questionsFile, mode='a', newline='', encoding='utf-8') as questions:
                questionWriter = csv.writer(questions, delimiter=';')
                questionWriter.writerow([self.question, self.correctAnswer, self.badAnswers[0], self.badAnswers[1], self.badAnswers[2]])
        except:
            pygame.quit()
            exit("Not found file" + questionsFile)
    def ToButtons(self):
        buttons = list()
        texts = [self.correctAnswer, self.badAnswers[0], self.badAnswers[1], self.badAnswers[2]]
        random.shuffle(texts)
        texts.insert(0, self.question)
        self.correctAnswerIndex = texts.index(self.correctAnswer)
        print(self.correctAnswerIndex)
        for i in range(5):
            buttons.append(ButtonWithText(emptyButtonFile, questionButtonCoordinates[i][0], questionButtonCoordinates[i][1], standardButtonWidth, standardButtonHeight, texts[i]))
        return buttons


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
    firstScreen = Screen(firstScreenDisplay, (71, 174, 56), MainMenuButtonsLoader(), None)
    current_display.currentScreen = firstScreen
    current_display.currentButtons = firstScreen.buttons

def AddQuestionLabelsLoader():
    labelsList = list()
    try:
        with open(addQuestionLabelsFile, mode='r', encoding='utf-8-sig') as labels:
            labels = csv.reader(labels, delimiter=';')
            for row in labels:
               labelsList.append(Label(row[0], int(row[1]), int(row[2]), int(row[3])))
    except:
        pygame.quit()
        exit("Not found file: " + addQuestionLabelsFile)
    return labelsList




def AddQuestionButtonsLoader():
    buttonList = list()
    for i in range(5):
        try:
            buttonList.append(ButtonWithText(emptyButtonFile, questionButtonCoordinates[i][0], questionButtonCoordinates[i][1], standardButtonWidth, standardButtonHeight, ""))
        except:
           pygame.quit()
           exit("Not found file " + emptyButtonFile)
    try:
        buttonList.append(Button(cancelButtonFile, 100, 800, standardButtonWidth, standardButtonHeight))
    except:
        pygame.quit()
        exit("Not found file " + cancelButtonFile)
    try:
        buttonList.append(Button(confirmButtonFile, windowWidth - 100 - standardButtonWidth, 800, standardButtonWidth, standardButtonHeight))
    except:
        pygame.quit()
        exit("Not found file " + confirmButtonFile)
    return buttonList

def AddQuestionScreenSetup():
    import current_display
    addQuestionScreenDisplay = pygame.display.set_mode((windowWidth, windowHeight))
    addQuestionScreen = Screen(addQuestionScreenDisplay, (71, 174, 56), AddQuestionButtonsLoader(), AddQuestionLabelsLoader())
    current_display.currentScreen = addQuestionScreen
    current_display.currentButtons = addQuestionScreen.buttons

def LoadQuestions():
    questionsList = list()
    try:
        with open(questionsFile, mode='r', encoding='utf-8-sig') as questions:
            questions = csv.reader(questions, delimiter=';')
            for row in questions:
                questionsList.append(Question(row[0], row[1], (row[2], row[3], row[4])))
    except:
        pygame.quit()
        exit("Not found file: " + questionsFile)
    random.shuffle(questionsList)
    questionsList = questionsList[:15]
    return questionsList

def GameScreenSetup():
    import current_display
    current_display.currentQuestions = LoadQuestions()
    current_display.currentQuestion = 0
    playGameScreenDisplay = pygame.display.set_mode((windowWidth, windowHeight))
    playGameScreen = Screen(playGameScreenDisplay, (71, 174, 56), current_display.currentQuestions[0].ToButtons(), None)
    current_display.currentScreen = playGameScreen
    current_display.currentButtons = playGameScreen.buttons
