current_screen = None  # Instance of Class game_loader.Screen, meaning current window

current_buttons = None  # List of instances of game_loader.Button, current showed buttons. Some may be clickable

current_questions = None  # List of instances of game_loader.Question, 15 questions for this game

current_question = 0  # Current index of question (+1 with every correct answer)

score = 0

# Available hints

fifty_fifty_available = True

friend_help_available = True

public_help_available = True


def display_screen():  # Displays current_screen
    current_screen.draw()


def determine_clicked_button(mouse_position):  # Returns index of the clicked-on button within current_buttons
    i = 0
    for button in current_buttons:
        if button is not None and button.mouse_collision(mouse_position):
            return i
        i += 1
    return -1  # Returns -1 if none of buttons is clicked on
