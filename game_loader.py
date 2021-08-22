import pygame
import os
import csv
import random

# Constants of window and buttons

window_width = 1280
window_height = 1040
standard_button_width = 361
standard_button_height = 114
wide_button_width = 801
wide_button_height = 50
small_button_side = 30

background = (71, 174, 56)  # RGB background colour

scores = ['0', '100', '200', '300', '500', '1 000', '2 000', '4 000', '8 000', '16 000', '32 000', '64 000', '125 000',
          '250 000', '500 000', '1 000 000']  # Game scores

# Constants with files relative paths

main_menu_buttons_dir = "assets/Menu_buttons/"
icon_file = "assets/football.png"
empty_button_file = "assets/emptyButton.png"
wide_empty_button_file = "assets/wideEmptyButton.png"
confirm_button_file = "assets/confirmButton.png"
cancel_button_file = "assets/cancelButton.png"
back_to_menu_button_file = "assets/backToMenuButton.png"
end_game_button_file = "assets/endGameButton.png"
fifty_fifty_button = "assets/hintButtons/fiftyFifty.png"
friend_help_button = "assets/hintButtons/friendHelp.png"
public_help_button = "assets/hintButtons/publicHelp.png"
questions_file = "questions.csv"
highscores_file = "highscores.csv"
add_question_labels_file = "labels/addQuestionLabels.csv"
play_game_labels_file = "labels/playGameLabels.csv"
loss_game_labels_file = "labels/lossGameLabels.csv"
win_game_labels_file = "labels/winGameLabels.csv"
highscores_labels_file = "labels/highscoresLabels.csv"
friend_help_labels_file = "labels/friendHelpLabels.csv"
public_help_bar_chart = "assets/helpBarChart.png"
font_file = "assets/Caveat-VariableFont_wght.ttf"  # From Google Fonts

# Coordinates on which are buttons placed by a question

question_button_coordinates = [((window_width - standard_button_width) / 2, 200), (200, 400),
                               (window_width - 200 - standard_button_width, 400), (200, 600),
                               (window_width - 200 - standard_button_width, 600)]


class Screen:  # Class of a screen to display
    def __init__(self, screen_display, buttons, labels_list):
        self.display = screen_display   # Instance of pygame.display
        self.background = background  # Background colour, defined in constants
        self.buttons = buttons  # Buttons of the screen (list of instances of Class Button)
        self.labels = labels_list  # Labels of the screen (list of instances of Class Label)

    def draw(self):  # Displays all buttons and labels on the background
        self.display.fill(self.background)
        if self.buttons is not None:
            for button in self.buttons:
                if button is not None:
                    button.blit_on_screen(self.display)
        if self.labels is not None:
            for label in self.labels:
                label.show(self.display)

    def show_arrow(self, current_question):  # Shows arrow by the label on question index
        self.labels[14 - current_question].add_arrow()

    def hide_arrow(self, current_question):  # Hides arrow by the label on question index
        self.labels[14 - current_question].hide_arrow()


class Button:  # Class of a image, which may be clickable and act like a button, but doesn't have to
    def __init__(self, file, x_axis, y_axis, width, height):
        self.file = pygame.image.load(file)  # File of the source image
        self.XAxis = x_axis  # Position on screen
        self.YAxis = y_axis
        self.width = width  # Dimensions
        self.height = height

    def blit_on_screen(self, display):  # Shows the button (image) on given display
        display.blit(self.file, (self.XAxis, self.YAxis))

    def mouse_collision(self, mouse_position):  # Determines whether cursor is inside of the button
        return self.XAxis <= mouse_position[0] <= (self.XAxis + self.width) and self.YAxis <= mouse_position[1] <=\
                (self.YAxis + self.height)  # Returns True or False


class ButtonWithText(Button):  # Class of a Button, that can be filled with texts. Inherits from Class Button
    def __init__(self, file, x_axis, y_axis, width, height, text, maximum_chars, maximum_per_row):
        super().__init__(file, x_axis, y_axis, width, height)  # These parameters stay, but text and maximums are added
        self.clickedOn = False  # clickedOn determines, whether user is writing on this button
        self.cursorPosition = 0  # Cursor position marks where the cursor ('|') is
        self.maximumChars = maximum_chars  # Maximum of chars in this button
        self.maximumPerRow = maximum_per_row  # Maximum of chars in one row. Standard button has 34, wide has 50
        try:  # font of the text is collected from assets. If it can't be reached, normal font is used instead
            self.font = pygame.font.Font(font_file, 25)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, 25)
        self.text = text  # Text of the button, which gets displayed

    def blit_on_screen(self, display):
        super(ButtonWithText, self).blit_on_screen(display)
        text_parts = list()
        for i in range((len(self.text) // self.maximumPerRow) + 1):  # for i in range (number of rows)
            if i != (len(self.text) // self.maximumPerRow) + 1:  # if i != last row
                text_parts.append(self.text[i * self.maximumPerRow:((i + 1) * self.maximumPerRow)])  # Appends row
        for i in range(len(text_parts)):  # Every row apart from the last one
            if i != len(text_parts) - 1:  # Gets rid of everything after the last space
                if " " in text_parts[i]:
                    while not (text_parts[i].endswith(' ')):  # If row doesn't end with " ", char is transferred
                        text_parts[i + 1] = text_parts[i][-1] + text_parts[i + 1]          # to previous row
                        text_parts[i] = text_parts[i][:-1]
            # This is done to prevent break-rows in middle of words
            text = self.font.render(text_parts[i], True, (0, 0, 0), (255, 255, 255))  # Text gets shown black on white
            text_rect = text.get_rect()
            text_rect.center = (self.XAxis + self.width / 2, self.YAxis + 20 + i * 36)
            display.blit(text, text_rect)

    # Cursor in this little text editor is a char '|'
    def show_cursor(self, replace_mode=0):  # Shows cursor, may also delete chars with replace mode
        self.text = self.text.replace("|", "")  # Hides cursor first
        if replace_mode == 0:  # Cursor appears on its position
            self.text = self.text[:self.cursorPosition] + '|' + self.text[self.cursorPosition:]
        elif replace_mode == 1:  # Cursor appears and previous char gets deleted
            self.text = self.text[:self.cursorPosition - 1] + '|' + self.text[self.cursorPosition:]
        elif replace_mode == 2:  # Cursor appears and next char gets deleted
            self.text = self.text[:self.cursorPosition] + '|' + self.text[self.cursorPosition + 1:]

    def hide_cursor(self):  # Hides cursor
        self.text = self.text.replace('|', "")

    def add_char(self, key):  # Adds character on the place of cursor
        if (len(self.text)) == self.maximumChars or key == "|":
            return  # If the text is too long or player wants to add '|' (our cursor), the char doesn't get added
        old_string = self.text
        self.text = self.text.replace("|", key)                      # New cursor position is calculate through lengths
        self.cursorPosition += len(self.text) - len(old_string) + 1  # of previous and current text
        self.show_cursor()  # Cursor reappears

    # Operation functions
    def remove_previous(self):  # Deletes last char, done via show_cursor method
        if self.cursorPosition == 0:
            return  # If on first position, nothing happens
        self.show_cursor(1)
        self.move_cursor_left()  # Also moves cursor left

    def remove_next(self):  # Deletes last char, done via show_cursor method
        if self.cursorPosition == len(self.text) - 1:
            return  # If on last position, nothing happens
        self.show_cursor(2)

    def move_cursor_left(self, max=False):  # Moves cursor to start or one left
        if max or self.cursorPosition == 0:
            self.cursorPosition = 0
        else:
            self.cursorPosition -= 1
        self.show_cursor()

    def move_cursor_right(self, max=False):  # Moves cursor to end or one right
        if max or self.cursorPosition == len(self.text) - 1:
            self.cursorPosition = len(self.text) - 1
        else:
            self.cursorPosition += 1
        self.show_cursor()


class Label:  # Text showed on screen on certain position
    def __init__(self, text, text_size, x_axis, y_axis):
        try:  # Font is obtained from a file, if it can't be reached. Default font is used instead
            self.font = pygame.font.Font(font_file, text_size)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, text_size)
        self.text = text
        self.textGraphic = self.font.render(self.text, True, (255, 255, 255), background)
        self.textRect = self.textGraphic.get_rect()
        self.textRect.center = (x_axis, y_axis)

    def show(self, display):  # Shows text on its position
        display.blit(self.textGraphic, self.textRect)

    def add_arrow(self):  # Adds arrow (necessary for scores to show the current one)
        self.text = "->   " + self.text
        self.textGraphic = self.font.render(self.text, True, (255, 255, 255), background)

    def hide_arrow(self):  # Hides the arrow
        self.text = self.text[4:]
        self.textGraphic = self.font.render(self.text, True, (255, 255, 255), background)


class Question:  # Class of one question. Holds the question itself and its answers. Enables saving and using of hints
    def __init__(self, question, correct_answer, bad_answers):
        self.question = question
        self.correctAnswer = correct_answer
        self.badAnswers = bad_answers
        self.correctAnswerIndex = 1
        self.answersInOrder = None
        self.fiftyFiftyUsed = False

    def write_to_csv(self):  # Saves question to questions.csv
        try:
            with open(questions_file, mode='a', newline='', encoding='utf-8') as questions:
                question_writer = csv.writer(questions, delimiter=';')
                question_writer.writerow(  # Writes a row: Question;CorrectAnswer;Bad;Ans;wers
                    [self.question, self.correctAnswer, self.badAnswers[0], self.badAnswers[1], self.badAnswers[2]])
        # If file doesn't exist or we can't write here, question doesn't gets saved
        except FileNotFoundError:
            pass
        except PermissionError:
            pass

    def to_buttons(self, order_is_set=False):  # Displays this question as buttons
        buttons = list()
        if not order_is_set:  # Answers are randomly organised
            texts = [self.correctAnswer, self.badAnswers[0], self.badAnswers[1], self.badAnswers[2]]
            random.shuffle(texts)
            self.answersInOrder = texts
            texts.insert(0, self.question)
            self.correctAnswerIndex = texts.index(self.correctAnswer)
        if self.fiftyFiftyUsed:  # If fiftyFifty hint was used. Two random bad answers are hid
            rnd1 = random.randint(0, 3)
            rnd2 = random.randint(0, 3)
            while rnd1 == self.correctAnswerIndex - 1 or rnd2 == self.correctAnswerIndex - 1 or rnd1 == rnd2:
                rnd1 = random.randint(0, 3)
                rnd2 = random.randint(0, 3)
            self.answersInOrder[rnd1 + 1] = ""
            self.answersInOrder[rnd2 + 1] = ""
        for i in range(5):  # Questions and answers are displayed as ButtonWithTexts
            buttons.append(
                ButtonWithText(empty_button_file, question_button_coordinates[i][0], question_button_coordinates[i][1],
                               standard_button_width, standard_button_height, self.answersInOrder[i], 100, 33))
        buttons.append(Button(end_game_button_file, (window_width - standard_button_width) / 2, 800,
                              standard_button_width, standard_button_height))  # Button number six is "End Game" button
        import current_display
        # Here we continue with displaying hints' buttons. Only hints that are available get their button displayed
        if current_display.fifty_fifty_available:
            buttons.append(Button(fifty_fifty_button, (window_width - small_button_side) / 2 - 100, 50,
                                  small_button_side, small_button_side))
        else:
            buttons.append(None)  # If hint isn't available, None gets appended
        if current_display.friend_help_available:
            buttons.append(
                Button(friend_help_button, (window_width - small_button_side) / 2, 50, small_button_side,
                       small_button_side))
        else:
            buttons.append(None)
        if current_display.public_help_available:
            buttons.append(Button(public_help_button, (window_width - small_button_side) / 2 + 100, 50,
                                  small_button_side, small_button_side))
        else:
            buttons.append(None)

        return buttons

    def friend_help(self, question_index):  # Method of friend help, returns new labels -> dialog with imaginary friend
        new_labels = list()
        possible_texts = list()
        with open(friend_help_labels_file, mode='r', encoding='utf-8-sig') as labels:
            labels = csv.reader(labels, delimiter=';')  # Possible labels get loaded from a file
            i = 0
            display_row = 0  # Row of the text on which should be the label displayed
            for row in labels:
                if i < 4:
                    new_labels.append(Label(row[0], 22, 225, 20 + 30 * display_row))
                elif i == 4:
                    new_labels.append(Label(row[0], 22, 225, 20 + 30 * display_row))
                    if len(self.question) > 50:  # If question is too long, it is split to two lines
                        text_parts = [self.question[:50], self.question[50:]]
                        while not text_parts[0].endswith(' '):
                            text_parts[1] = text_parts[0][-1] + text_parts[1]
                            text_parts[0] = text_parts[0][:-1]
                        display_row += 1
                        new_labels.append(Label(text_parts[0], 22, 225, 20 + 30 * display_row))
                        display_row += 1
                        new_labels.append(Label(text_parts[1], 22, 225, 20 + 30 * display_row))
                    else:
                        display_row += 1
                        new_labels.append(Label(self.question, 22, 225, 20 + 30 * display_row))
                elif i == 5:
                    new_labels.append(Label(row[0], 22, 225, 20 + 30 * display_row))
                else:
                    possible_texts.append(row[0])
                i += 1
                display_row += 1
            import current_display
            for i in range(1, 5):  # Adds current possible answers
                if current_display.current_buttons[i].text != "":
                    new_labels.append(Label(current_display.current_buttons[i].text, 20, 225, 230 + 25 * i))
                    display_row += 1

            friends_knowledge = random.randint(0, 40)  # Random number between 0 and 40
            friends_knowledge -= question_index  # Gets lowered by current question index (the further we are,
            if friends_knowledge >= 30:           # the smaller chance of getting the correct answer)
                new_labels.append(Label(possible_texts[0] + self.correctAnswer, 22, 225, 375))  # 30 - 39, 100 % correct
            elif friends_knowledge >= 10:  # 10 - 29, friend says the correct answer, but isn't 100 % sure
                new_labels.append(Label(possible_texts[1] + self.correctAnswer, 22, 225, 375))
            elif friends_knowledge >= 5:  # 5 - 9, friend doesn't know. Doesn't say anything useful
                new_labels.append(Label(possible_texts[2], 22, 225, 375))
            else:  # Smaller than 5, friend says incorrect answer. Same sentence as in 15 - 29 scenario,
                import current_display                                      # but with different answer
                rnd = random.randint(0, 2)  # The answer is randomly picked
                current_answers = list()
                for i in range(1, 5):
                    current_answers.append(current_display.current_buttons[i].text)
                while self.badAnswers[rnd] not in current_answers:  # Can't say answer which was moved out by 50/50 hint
                    rnd = random.randint(0, 2)
                new_labels.append(Label(possible_texts[1] + self.badAnswers[rnd], 22, 225, 375))
        return new_labels

    def public_help(self, question_index):  # Method of public help
        import matplotlib.pyplot as plot
        import current_display
        current_answers = list()
        percentages = list()
        correct_answer_percentage = random.randint(85 - 4 * question_index, 100 - 3 * question_index)
        # Percentage to correct answer is given randomly. The boundaries are determined by question_index
        remaining_percentage = 100 - correct_answer_percentage  # The remaining percentage is split between other
        for i in range(1, 5):
            if current_display.current_buttons[i].text != "":
                current_answers.append(current_display.current_buttons[i].text)
        if len(current_answers) == 2:
            percentages.append(remaining_percentage)
        else:
            for i in range(3):
                percentage = random.randint(0, remaining_percentage)
                percentages.append(percentage)
                remaining_percentage -= percentage
        percentages.insert(self.correctAnswerIndex - 1, correct_answer_percentage)  # Correct answer is inserted on
        plot.figure()                 # hex-background                                correct position
        plot.rcParams['axes.facecolor'] = '#47ae38'  # Face colour of bar chart is given same colour as background is
        plot.bar(current_answers, percentages, color='white')  # Bars of the graph are white
        plot.xticks(rotation=30)
        plot.tight_layout()  # Tight layout to make sure, that all answers fit in the graph
        plot.savefig(public_help_bar_chart, dpi=50)  # Graph is saved to .png file
        button = Button(public_help_bar_chart, 50, 750, 320, 240)  # File is used to create button
        os.remove(public_help_bar_chart)  # The file is now deleted
        return button  # Button is returned


def general_setup():  # Setup of the window
    pygame.display.set_caption("Football Trivia")  #Title
    try:  # If icon is not found, default icon is used
        icon = pygame.image.load(icon_file)
        pygame.display.set_icon(icon)
    except FileNotFoundError:
        pass
    first_screen_setup()  # Main menu is set up


def load_questions():  # Loads random 15 questions from file questions.csv
    questions_list = list()
    try:
        with open(questions_file, mode='r', encoding='utf-8-sig') as questions:
            questions = csv.reader(questions, delimiter=';')
            for row in questions:
                questions_list.append(Question(row[0], row[1], (row[2], row[3], row[4])))
    except FileNotFoundError:
        pygame.quit()
        exit("Not found file: " + questions_file)
    random.shuffle(questions_list)
    questions_list = questions_list[:15]
    return questions_list


def write_score(nickname, score):  # Writes score with this nickname to highscores.csv
    from datetime import datetime
    from operator import itemgetter
    scores_list = list()
    # Reads current scores from file
    try:
        with open(highscores_file, mode='r', encoding='utf-8-sig') as highscores:
            highscores = csv.reader(highscores, delimiter=';')
            for row in highscores:
                scores_list.append([row[0], scores.index(row[1]), row[2]])
        scores_list.append([nickname, scores.index(score), datetime.now().strftime("%d.%m.%Y %H:%M")])
        sorted_scores = sorted(scores_list, key=itemgetter(1), reverse=True)  # Sorts the score
        sorted_scores = sorted_scores[:10]  # Only Top 10 results are displayed
    except FileNotFoundError:
        open(highscores_file, mode='x')  # If the file doesn't exist, it gets created
        scores_list.append([nickname, scores.index(score), datetime.now().strftime("%d.%m.%Y %H:%M")])
        sorted_scores = sorted(scores_list, key=itemgetter(1), reverse=True)
    # Writes the scores from list to file
    try:
        with open(highscores_file, mode='w', encoding='utf-8-sig', newline='') as highscores:
            highscores = csv.writer(highscores, delimiter=';', )
            for row in sorted_scores:
                row[1] = scores[row[1]]
                highscores.writerow(row)
    except FileNotFoundError:  # If, for some reason, the file can't be reached, or there can't be written any text
        pass                   # the score is not saved
    except PermissionError:
        pass

# Functions that set up screens and their buttons/labels


def first_screen_setup():
    import current_display
    first_screen_display = pygame.display.set_mode((window_width, window_height))
    first_screen = Screen(first_screen_display, main_menu_buttons_loader(), None)
    current_display.current_screen = first_screen
    current_display.current_buttons = first_screen.buttons


def main_menu_buttons_loader():
    button_list = list()
    i = 0
    for file in os.listdir(main_menu_buttons_dir):
        try:
            button_list.append(
                Button(main_menu_buttons_dir + file, (window_width - standard_button_width) / 2, 200 + (i * 200),
                       standard_button_width, standard_button_height))
        except NotADirectoryError:
            pygame.quit()
            exit("Not found directory: " + main_menu_buttons_dir)
        i += 1
    return button_list


def add_question_screen_setup():
    import current_display
    add_question_screen_display = pygame.display.set_mode((window_width, window_height))
    add_question_screen = Screen(add_question_screen_display, add_question_buttons_loader(),
                                 add_question_labels_loader())
    current_display.current_screen = add_question_screen
    current_display.current_buttons = add_question_screen.buttons


def add_question_labels_loader():
    labels_list = list()
    try:
        with open(add_question_labels_file, mode='r', encoding='utf-8-sig') as labels:
            labels = csv.reader(labels, delimiter=';')
            for row in labels:
                labels_list.append(Label(row[0], int(row[1]), int(row[2]), int(row[3])))
    except FileNotFoundError:
        pygame.quit()
        exit("Not found file: " + add_question_labels_file)
    return labels_list


def add_question_buttons_loader():
    button_list = list()
    for i in range(5):
        try:
            button_list.append(
                ButtonWithText(empty_button_file, question_button_coordinates[i][0], question_button_coordinates[i][1],
                               standard_button_width, standard_button_height, "", 100, 34))
        except FileNotFoundError:
            pygame.quit()
            exit("Not found file " + empty_button_file)
    try:
        button_list.append(Button(cancel_button_file, 100, 800, standard_button_width, standard_button_height))
    except FileNotFoundError:
        pygame.quit()
        exit("Not found file " + cancel_button_file)
    try:
        button_list.append(Button(confirm_button_file, window_width - 100 - standard_button_width, 800,
                                  standard_button_width, standard_button_height))
    except FileNotFoundError:
        pygame.quit()
        exit("Not found file " + confirm_button_file)
    return button_list


def game_setup():
    import current_display
    current_display.current_questions = load_questions()
    current_display.current_question = 0
    current_display.fifty_fifty_available = True
    current_display.friend_help_available = True
    current_display.public_help_available = True
    buttons = current_display.current_questions[0].to_buttons()
    play_game_screen_display = pygame.display.set_mode((window_width, window_height))
    play_game_screen = Screen(play_game_screen_display, buttons, play_game_labels_loader())
    play_game_screen.show_arrow(0)
    current_display.current_screen = play_game_screen
    current_display.current_buttons = play_game_screen.buttons


def play_game_labels_loader():
    labels_list = list()
    i = 0
    try:
        with open(play_game_labels_file, mode='r', encoding='utf-8-sig') as labels:
            labels = csv.reader(labels, delimiter=';')
            for row in labels:
                labels_list.append(Label(row[0], int(row[1]), int(row[2]), int(row[3])))
                i += 1
    except FileNotFoundError:
        pygame.quit()
        exit("File not found: " + play_game_labels_file)
    return labels_list


def highscores_screen_setup():
    import current_display
    highscores_screen_display = pygame.display.set_mode((window_width, window_height))
    highscores_screen = Screen(highscores_screen_display, None, highscores_labels_loader())
    current_display.current_screen = highscores_screen
    current_display.current_buttons = None


def highscores_labels_loader():
    labels_list = list()
    try:
        with open(highscores_labels_file, mode='r', encoding='utf-8-sig') as labels:
            labels = csv.reader(labels, delimiter=';')
            i = 0
            for row in labels:
                labels_list.append(Label(row[0], int(row[1]), int(row[2]), int(row[3])))
                i += 1
    except FileNotFoundError:
        pygame.quit()
        exit("File not found: " + highscores_labels_file)

    try:
        with open(highscores_file, mode='r', encoding='utf-8-sig') as highscores:
            highscores = csv.reader(highscores, delimiter=';')
            position = 1
            for row in highscores:
                labels_list.append(
                    Label(("%s. %s        %s        %s" % (position, row[0], row[1], row[2])), 22, window_width / 2,
                          300 + position * 25))
                position += 1
            labels_list.pop(1)
    except FileNotFoundError:
        labels_list.pop(0)
    return labels_list


def loss_game_screen_setup(correct_answer, score):
    import current_display
    loss_game_screen_display = pygame.display.set_mode((window_width, window_height))
    loss_game_screen = Screen(loss_game_screen_display, end_game_buttons_loader(),
                              loss_game_labels_loader(correct_answer, score))
    current_display.current_screen = loss_game_screen
    current_display.current_buttons = loss_game_screen.buttons


def win_game_screen_setup():
    import current_display
    win_game_screen_display = pygame.display.set_mode((window_width, window_height))
    win_game_screen = Screen(win_game_screen_display, end_game_buttons_loader(), win_game_labels_loader())
    current_display.current_screen = win_game_screen
    current_display.current_buttons = win_game_screen.buttons


def end_game_buttons_loader():
    buttons_list = list()
    buttons_list.append(
        ButtonWithText(wide_empty_button_file, (window_width - wide_button_width) / 2, 400, wide_button_width,
                       wide_button_height, "", 50, 50))
    buttons_list.append(Button(back_to_menu_button_file, 200, 600, standard_button_width, standard_button_height))
    buttons_list.append(Button(confirm_button_file, window_width - 200 - standard_button_width, 600,
                               standard_button_width, standard_button_height))
    return buttons_list


def loss_game_labels_loader(correct_answer, score):
    labels_list = list()
    try:
        with open(loss_game_labels_file, mode='r', encoding='utf-8-sig') as labels_file:
            labels_file = csv.reader(labels_file, delimiter=';')
            i = 0
            for row in labels_file:
                if i == 1:
                    row[0] += correct_answer
                if i == 2:
                    row[0] += str(score)
                labels_list.append(Label(row[0], int(row[1]), int(row[2]), int(row[3])))
                i += 1
    except FileNotFoundError:
        pygame.quit()
        exit("Not found file: " + loss_game_labels_file)

    return labels_list


def win_game_labels_loader():
    labels_list = list()
    try:
        with open(win_game_labels_file, mode='r', encoding='utf-8-sig') as labels_file:
            labels_file = csv.reader(labels_file, delimiter=';')
            for row in labels_file:
                labels_list.append(Label(row[0], int(row[1]), int(row[2]), int(row[3])))
    except FileNotFoundError:
        pygame.quit()
        exit("File not found: " + win_game_labels_file)

    return labels_list
