import pygame
import os
import csv
import random

windowWidth = 1280
windowHeight = 1040
standardButtonWidth = 361
standardButtonHeight = 114
wideButtonWidth = 801
wideButtonHeight = 50

background = (71, 174, 56)

scores = [0, 100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]

mainMenuButtonsDir = "assets/Menu_buttons/"
iconFile = "assets/football.png"
emptyButtonFile = "assets/emptyButton.png"
wideEmptyButtonFile = "assets/wideEmptyButton.png"
confirmButtonFile = "assets/confirmButton.png"
cancelButtonFile = "assets/cancelButton.png"
backToMenuButtonFile = "assets/backToMenuButton.png"
questionsFile = "questions.csv"
highscoresFile = "highscores.csv"
addQuestionLabelsFile = "labels/addQuestionLabels.csv"
playGameLabelsFile = "labels/playGameLabels.csv"
lossGameLabelsFile = "labels/lossGameLabels.csv"
fontFile = "assets/Caveat-VariableFont_wght.ttf"  # Ze stránky Google Fonts

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
    def ShowArrow(self, currentQuestion):
        self.labels[14 - currentQuestion].AddArrow()

    def HideArrow(self, currentQuestion):
        self.labels[14 - currentQuestion].HideArrow()


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
    def __init__(self, file, x_axis, y_axis, width, height, text, maximumChars, maximumPerRow):
        super().__init__(file, x_axis, y_axis, width, height)
        self.clickedOn = False
        self.cursorPosition = 0
        self.maximumChars = maximumChars
        self.maximumPerRow = maximumPerRow
        try:
            self.font = pygame.font.Font(fontFile, 25)
        except:
            self.font = pygame.font.Font(None, 25)
        self.text = text

    def BlitOnScreen(self, display):
        super(ButtonWithText, self).BlitOnScreen(display)
        textParts = list()
        for i in range((len(self.text) // self.maximumPerRow) + 1):
            if i != 4:
                textParts.append(self.text[i * self.maximumPerRow:((i + 1) * self.maximumPerRow )])
        for i in range(len(textParts)):
            if i != len(textParts) - 1:
                if " " in textParts[i]:
                    while not (textParts[i].endswith(' ')):
                        textParts[i + 1] = textParts[i][-1] + textParts[i + 1]
                        textParts[i] = textParts[i][:-1]

            text = self.font.render(textParts[i], True, (0, 0, 0), (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (self.XAxis + self.width / 2, self.YAxis + 20 + i * 36)
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
        if (len(self.text)) == self.maximumChars or key == "|":
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
        self.text = text
        self.textGraphic = self.font.render(self.text, True, (255, 255, 255), background)
        self.textRect = self.textGraphic.get_rect()
        self.textRect.center = (x_axis, y_axis)

    def Show(self, display):
        display.blit(self.textGraphic, self.textRect)

    def AddArrow(self):
        self.text = "->   " + self.text
        self.textGraphic = self.font.render(self.text, True, (255, 255, 255), background)

    def HideArrow(self):
        self.text = self.text[4:]
        self.textGraphic = self.font.render(self.text, True, (255, 255, 255), background)

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
            exit("Not found file " + questionsFile)
    def ToButtons(self):
        buttons = list()
        texts = [self.correctAnswer, self.badAnswers[0], self.badAnswers[1], self.badAnswers[2]]
        random.shuffle(texts)
        texts.insert(0, self.question)
        self.correctAnswerIndex = texts.index(self.correctAnswer)
        for i in range(5):
            buttons.append(ButtonWithText(emptyButtonFile, questionButtonCoordinates[i][0], questionButtonCoordinates[i][1], standardButtonWidth, standardButtonHeight, texts[i], 100, 33))
        buttons.append(Button(backToMenuButtonFile, (windowWidth - standardButtonWidth) / 2, 800, standardButtonWidth,
                              standardButtonHeight))

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
    buttonList = list()
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
    firstScreen = Screen(firstScreenDisplay, background, MainMenuButtonsLoader(), None)
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
            buttonList.append(ButtonWithText(emptyButtonFile, questionButtonCoordinates[i][0], questionButtonCoordinates[i][1], standardButtonWidth, standardButtonHeight, "", 100, 34))
        except FileNotFoundError:
           pygame.quit()
           exit("Not found file " + emptyButtonFile)
    try:
        buttonList.append(Button(cancelButtonFile, 100, 800, standardButtonWidth, standardButtonHeight))
    except FileNotFoundError:
        pygame.quit()
        exit("Not found file " + cancelButtonFile)
    try:
        buttonList.append(Button(confirmButtonFile, windowWidth - 100 - standardButtonWidth, 800, standardButtonWidth, standardButtonHeight))
    except FileNotFoundError:
        pygame.quit()
        exit("Not found file " + confirmButtonFile)
    return buttonList


def AddQuestionScreenSetup():
    import current_display
    addQuestionScreenDisplay = pygame.display.set_mode((windowWidth, windowHeight))
    addQuestionScreen = Screen(addQuestionScreenDisplay, background, AddQuestionButtonsLoader(), AddQuestionLabelsLoader())
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


def PlayGameLabels():
    labelsList = list()
    i = 0
    try:
        with open(playGameLabelsFile, mode='r', encoding='utf-8-sig') as labels:
            labels = csv.reader(labels, delimiter=';')
            for row in labels:
                labelsList.append(Label(row[0], int(row[1]), int(row[2]), int(row[3])))
                i += 1
    except:
        pygame.quit()
        exit("File not found: " + playGameLabelsFile)
    return labelsList



def GameScreenSetup():
    import current_display
    current_display.currentQuestions = LoadQuestions()
    current_display.currentQuestion = 0
    buttons = current_display.currentQuestions[0].ToButtons()
    playGameScreenDisplay = pygame.display.set_mode((windowWidth, windowHeight))
    playGameScreen = Screen(playGameScreenDisplay, background, buttons, PlayGameLabels())
    playGameScreen.ShowArrow(0)
    current_display.currentScreen = playGameScreen
    current_display.currentButtons = playGameScreen.buttons

def WriteScore(nickname, score):
    from datetime import datetime
    # i = 0
    # try:
    #     with open(highscoresFile, mode='a', encoding='utf-8-sig', newline='') as highscores:
    #         highscores.write("\n" + nickname + "\t" + str(score))
    # except FileNotFoundError:
    #     pass
    try:
        from operator import itemgetter
        scoresList = list()
        with open(highscoresFile, mode='r', encoding='utf-8-sig') as highscores:
            highscores = csv.reader(highscores, delimiter=';')
            for row in highscores:
                scoresList.append([row[0], int(row[1]), row[2]])
        scoresList.append([nickname, score, datetime.now().strftime("%d.%m.%Y %H:%M")])
        sortedScores = sorted(scoresList, key=itemgetter(1), reverse=True)
        with open(highscoresFile, mode='w', encoding='utf-8-sig', newline='') as highscores:
            highscores = csv.writer(highscores, delimiter=';',)
            for row in sortedScores:
                highscores.writerow(row)
    except FileNotFoundError:
        pass
    except PermissionError:
        pass

def LossGameButtons():
    buttonsList = list()
    buttonsList.append(ButtonWithText(wideEmptyButtonFile, (windowWidth - wideButtonWidth) / 2, 400, wideButtonWidth, wideButtonHeight, "", 50, 50))
    buttonsList.append(Button(backToMenuButtonFile, 200, 600, standardButtonWidth, standardButtonHeight))
    buttonsList.append(Button(confirmButtonFile, windowWidth - 200 - standardButtonWidth, 600, standardButtonWidth, standardButtonHeight))
    return buttonsList

def LossGameLabels(correctAnswer, score):
    labelsList = list()
    try:
        with open(lossGameLabelsFile, mode='r', encoding='utf-8-sig') as labelsFile:
            labelsFile = csv.reader(labelsFile, delimiter=';')
            i = 0
            for row in labelsFile:
                if i == 1:
                    row[0] += correctAnswer
                if i == 2:
                    row[0] += str(score)
                labelsList.append(Label(row[0], int(row[1]), int(row[2]), int(row[3])))
                i += 1
    except FileNotFoundError:
        pygame.quit()
        exit("Not found file: " + lossGameLabelsFile)

    return labelsList

def LossGameScreenSetup(correctAnswer, score):
    import current_display
    lossGameScreenDisplay = pygame.display.set_mode((windowWidth, windowHeight))
    lossGameScreen = Screen(lossGameScreenDisplay, background, LossGameButtons(), LossGameLabels(correctAnswer, score))
    current_display.currentScreen = lossGameScreen
    current_display.currentButtons = lossGameScreen.buttons