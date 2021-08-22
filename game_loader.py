import time

import matplotlib
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
smallButtonSide = 30

background = (71, 174, 56)

scores = ['0', '100', '200', '300', '500', '1 000', '2 000', '4 000', '8 000', '16 000', '32 000', '64 000', '125 000',
          '250 000', '500 000', '1 000 000']

mainMenuButtonsDir = "assets/Menu_buttons/"
iconFile = "assets/football.png"
emptyButtonFile = "assets/emptyButton.png"
wideEmptyButtonFile = "assets/wideEmptyButton.png"
confirmButtonFile = "assets/confirmButton.png"
cancelButtonFile = "assets/cancelButton.png"
backToMenuButtonFile = "assets/backToMenuButton.png"
endGameButtonFile = "assets/endGameButton.png"
fiftyFiftyButton = "assets/hintButtons/fiftyFifty.png"
friendHelpButton = "assets/hintButtons/friendHelp.png"
publicHelpButton = "assets/hintButtons/publicHelp.png"
questionsFile = "questions.csv"
highscoresFile = "highscores.csv"
addQuestionLabelsFile = "labels/addQuestionLabels.csv"
playGameLabelsFile = "labels/playGameLabels.csv"
lossGameLabelsFile = "labels/lossGameLabels.csv"
winGameLabelsFile = "labels/winGameLabels.csv"
highscoresLabelsFile = "labels/highscoresLabels.csv"
friendHelpLabelsFile = "labels/friendHelpLabels.csv"
publicHelpBarChart = "assets/helpBarChart.png"
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
        if self.buttons is not None:
            for button in self.buttons:
                if button is not None:
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
        self.answersInOrder = None
        self.fiftyFiftyUsed = False

    def WriteToCSV(self):
        try:
            with open(questionsFile, mode='a', newline='', encoding='utf-8') as questions:
                questionWriter = csv.writer(questions, delimiter=';')
                questionWriter.writerow([self.question, self.correctAnswer, self.badAnswers[0], self.badAnswers[1], self.badAnswers[2]])
        except:
            pygame.quit()
            exit("Not found file " + questionsFile)


    def ToButtons(self, orderIsSet = False):
        buttons = list()
        if not orderIsSet:
            texts = [self.correctAnswer, self.badAnswers[0], self.badAnswers[1], self.badAnswers[2]]
            random.shuffle(texts)
            self.answersInOrder = texts
            texts.insert(0, self.question)
            self.correctAnswerIndex = texts.index(self.correctAnswer)
        if self.fiftyFiftyUsed:
            rnd1 = random.randint(0, 3)
            rnd2 = random.randint(0, 3)
            while rnd1 == self.correctAnswerIndex - 1 or rnd2 == self.correctAnswerIndex - 1 or rnd1 == rnd2:
                rnd1 = random.randint(0, 3)
                rnd2 = random.randint(0, 3)
            self.answersInOrder[rnd1 + 1] = ""
            self.answersInOrder[rnd2 + 1] = ""
        for i in range(5):
            buttons.append(ButtonWithText(emptyButtonFile, questionButtonCoordinates[i][0], questionButtonCoordinates[i][1], standardButtonWidth, standardButtonHeight, self.answersInOrder[i], 100, 33))
        buttons.append(Button(endGameButtonFile, (windowWidth - standardButtonWidth) / 2, 800, standardButtonWidth,
                              standardButtonHeight))
        import current_display
        if current_display.fiftyFiftyAvailable:
            buttons.append(Button(fiftyFiftyButton, (windowWidth - smallButtonSide) / 2 - 100, 50, smallButtonSide, smallButtonSide))
        else:
            buttons.append(None)
        if current_display.friendHelpAvailable:
            buttons.append(Button(friendHelpButton, (windowWidth - smallButtonSide) / 2, 50, smallButtonSide, smallButtonSide))
        else:
            buttons.append(None)
        if current_display.publicHelpAvailable:
            buttons.append(Button(publicHelpButton, (windowWidth - smallButtonSide) / 2 + 100, 50, smallButtonSide, smallButtonSide))
        else:
            buttons.append(None)

        return buttons

    def FriendHelp(self, questionIndex):
        newLabels = list()
        possibleTexts = list()
        with open(friendHelpLabelsFile, mode='r', encoding='utf-8-sig') as labels:
            labels = csv.reader(labels, delimiter=';')
            i = 0
            displayRow = 0
            for row in labels:
                if i < 4:
                    newLabels.append(Label(row[0], 22, 225, 20+30*displayRow))
                elif i == 4:
                    newLabels.append(Label(row[0], 22, 225, 20+30*displayRow))
                    if len(self.question) > 50:
                        textParts = [self.question[:50], self.question[50:]]
                        while not textParts[0].endswith(' '):
                            textParts[1] = textParts[0][-1] + textParts[1]
                            textParts[0] = textParts[0][:-1]
                        displayRow += 1
                        newLabels.append(Label(textParts[0], 22, 225, 20 + 30 * displayRow))
                        displayRow += 1
                        newLabels.append(Label(textParts[1], 22, 225, 20 + 30 * displayRow))
                    else:
                        displayRow += 1
                        newLabels.append(Label(self.question, 22, 225, 20 + 30 * displayRow))
                elif i == 5:
                    newLabels.append(Label(row[0], 22, 225, 20+30*displayRow))
                else:
                    possibleTexts.append(row[0])
                i += 1
                displayRow += 1
            import current_display
            for i in range(1, 5):
                if current_display.currentButtons[i].text != "":
                    newLabels.append(Label(current_display.currentButtons[i].text, 20, 225, 230+25*i))
                    displayRow += 1

            friendsKnowledge = random.randint(0, 40)
            friendsKnowledge -= questionIndex
            if friendsKnowledge > 30:
                newLabels.append(Label(possibleTexts[0] + self.correctAnswer, 22, 225, 375))
            elif friendsKnowledge > 15:
                newLabels.append(Label(possibleTexts[1] + self.correctAnswer, 22, 225, 375))
            elif friendsKnowledge > 5:
                newLabels.append(Label(possibleTexts[2], 22, 225, 375))
            else:
                import current_display
                rnd = random.randint(0, 2)
                currentAnswers = list()
                for i in range(1, 5):
                    currentAnswers.append(current_display.currentButtons[i].text)
                while self.badAnswers[rnd] not in currentAnswers:
                    rnd = random.randint(0, 2)
                newLabels.append(Label(possibleTexts[1] + self.badAnswers[rnd], 22, 225, 375))
        return newLabels

    def PublicHelp(self, questionIndex):
        import matplotlib.pyplot as plot
        import current_display
        currentAnswers = list()
        percentages = list()
        correctAnswerPercentage = random.randint((16 - (questionIndex / 2)) * 6, (98 - questionIndex * 2))
        remainingPercenatge = 100 - correctAnswerPercentage
        for i in range(1, 5):
            if current_display.currentButtons[i].text != "":
                currentAnswers.append(current_display.currentButtons[i].text)
        if len(currentAnswers) == 2:
            percentages.append(remainingPercenatge)
        else:
            for i in range(3):
                percentage = random.randint(0, remainingPercenatge)
                percentages.append(percentage)
                remainingPercenatge -= percentage
        percentages.insert(self.correctAnswerIndex - 1, correctAnswerPercentage)
        plot.figure()
        plot.rcParams['axes.facecolor'] = '#47ae38'
        plot.bar(currentAnswers, percentages, color='white')
        plot.xticks(rotation=30)
        plot.tight_layout()
        plot.savefig(publicHelpBarChart, dpi=50)
        button = Button(publicHelpBarChart, 50, 750, 320, 240)
        os.remove(publicHelpBarChart)
        return button

def GeneralSetup():
    pygame.display.set_caption("Football Trivia")
    try:
        icon = pygame.image.load(iconFile)
    except FileNotFoundError:
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



def GameSetup():
    import current_display
    current_display.currentQuestions = LoadQuestions()
    current_display.currentQuestion = 0
    current_display.fiftyFiftyAvailable = True
    current_display.friendHelpAvailable = True
    current_display.publicHelpAvailable = True
    buttons = current_display.currentQuestions[0].ToButtons()
    playGameScreenDisplay = pygame.display.set_mode((windowWidth, windowHeight))
    playGameScreen = Screen(playGameScreenDisplay, background, buttons, PlayGameLabels())
    playGameScreen.ShowArrow(0)
    current_display.currentScreen = playGameScreen
    current_display.currentButtons = playGameScreen.buttons

def WriteScore(nickname, score):
    from datetime import datetime
    try:
        from operator import itemgetter
        scoresList = list()
        with open(highscoresFile, mode='r', encoding='utf-8-sig') as highscores:
            highscores = csv.reader(highscores, delimiter=';')
            for row in highscores:
                scoresList.append([row[0], scores.index(row[1]), row[2]])
        scoresList.append([nickname, scores.index(score), datetime.now().strftime("%d.%m.%Y %H:%M")])
        sortedScores = sorted(scoresList, key=itemgetter(1), reverse=True)
        sortedScores = sortedScores[:10]
        with open(highscoresFile, mode='w', encoding='utf-8-sig', newline='') as highscores:
            highscores = csv.writer(highscores, delimiter=';',)
            for row in sortedScores:
                row[1] = scores[row[1]]
                highscores.writerow(row)
    except FileNotFoundError:
        pass
    except PermissionError:
        pass

def HighscoreLabels():
    labelsList = list()
    try:
        with open(highscoresLabelsFile, mode='r', encoding='utf-8-sig') as labels:
            labels = csv.reader(labels, delimiter=';')
            for row in labels:
                labelsList.append(Label(row[0], int(row[1]), int(row[2]), int(row[3])))
    except FileNotFoundError:
        pygame.quit()
        exit("Not found file: " + highscoresLabelsFile)

    try:
        with open(highscoresFile, mode='r', encoding='utf-8-sig') as highscores:
            highscores = csv.reader(highscores, delimiter=';')
            position = 1
            for row in highscores:
                labelsList.append(Label(("%s. %s        %s        %s" % (position, row[0], row[1], row[2])), 22, windowWidth / 2, 300 + position * 25))
                position += 1
    except FileNotFoundError:
        pygame.quit()
        exit("Not found file: " + highscoresFile)
    return labelsList


def EndGameButtons():
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

def WinGameLabels():
    labelsList = list()
    try:
        with open(winGameLabelsFile, mode='r', encoding='utf-8-sig') as labelsFile:
            labelsFile = csv.reader(labelsFile, delimiter=';')
            for row in labelsFile:
                labelsList.append(Label(row[0], int(row[1]), int(row[2]), int(row[3])))
    except FileNotFoundError:
        pygame.quit()
        exit("File not found: " + winGameLabelsFile)

    return labelsList

def LossGameScreenSetup(correctAnswer, score):
    import current_display
    lossGameScreenDisplay = pygame.display.set_mode((windowWidth, windowHeight))
    lossGameScreen = Screen(lossGameScreenDisplay, background, EndGameButtons(), LossGameLabels(correctAnswer, score))
    current_display.currentScreen = lossGameScreen
    current_display.currentButtons = lossGameScreen.buttons


def WinGameScreenSetup():
    import current_display
    winGameScreenDisplay = pygame.display.set_mode((windowWidth, windowHeight))
    winGameScreen = Screen(winGameScreenDisplay, background, EndGameButtons(), WinGameLabels())
    current_display.currentScreen = winGameScreen
    current_display.currentButtons = winGameScreen.buttons

def HighscoresScreenSetup():
    import current_display
    highscoresScreenDisplay = pygame.display.set_mode((windowWidth, windowHeight))
    highscoresScreen = Screen(highscoresScreenDisplay, background, None, HighscoreLabels())
    current_display.currentScreen = highscoresScreen
    current_display.currentButtons = None

