import pygame

import game_loader


def game_loop(state):
    if state == 0:  # First screen -> Main menu
        return main_menu_loop()
    elif state == 1:  # The game itself
        return play_game_loop()
    elif state == 2:  # End-game screen
        return end_game_loop()
    elif state == 3:  # Adding question
        return add_question_loop()
    elif state == 4:  # Highscores screen
        return best_scores_loop()


def main_menu_loop():  # state == 0
    import current_display
    current_display.display_screen()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Alt+F4 or X button
            return -1  # Returns -1: end of the game
        elif event.type == pygame.MOUSEBUTTONUP:  # Mouse-click
            clickedButtonNumber = current_display.determine_clicked_button(pygame.mouse.get_pos())  # Returns index of
            if clickedButtonNumber == 0:  # clicked button
                game_loader.game_setup()  # If clicked "Play game", state is set to 1
                return 1
            elif clickedButtonNumber == 1:
                game_loader.add_question_screen_setup()  # If clicked "Add Question" state is set to 3
                return 3
            elif clickedButtonNumber == 2:
                game_loader.highscores_screen_setup()  # If clicked "See Highscores" state is set to 4
                return 4
            elif clickedButtonNumber == 3:  # If clicked "Quit" state is set to -1, which means end of the game
                return -1
    return 0  # Else 0 stays as the state number, meaning this loop will continue


def play_game_loop():  # state == 1
    import current_display
    current_display.display_screen()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Alt+F4 or X button
            return -1  # Returns -1: end of the game
        elif event.type == pygame.MOUSEBUTTONUP:  # Mouse-click
            clickedButtonNumber = current_display.determine_clicked_button(pygame.mouse.get_pos())  # Returns index of
            # clicked button
            if clickedButtonNumber == current_display.current_questions[current_display.current_question]. \
                    correctAnswerIndex:  # If the clicked button is the one with correct answer
                if current_display.current_question != 14:  # Unless it is the final answer
                    current_display.current_screen.hide_arrow(current_display.current_question)  # Moves the arrow
                    current_display.current_question += 1  # Raises the number of current question
                    newQuestionButtons = current_display.current_questions[  # Loads the new question
                        current_display.current_question].to_buttons()
                    current_display.current_screen.buttons = newQuestionButtons
                    current_display.current_screen.labels = current_display.current_screen.labels[:15]  # Deletes labels
                    # of friend's help, if they are displayed at the screen
                    current_display.current_buttons = newQuestionButtons
                    current_display.current_screen.show_arrow(current_display.current_question)
                    return 1  # State stays the same, only question changes
                else:  # If this was the last question, the game is won
                    current_display.score = game_loader.scores[-1]  # Player gets the maximum score
                    game_loader.win_game_screen_setup()  # Win-game screen is set up
                    return 2  # State is changed to End-game screen
            elif clickedButtonNumber == 5:  # If the clicked button is "End game"
                current_display.score = game_loader.scores[current_display.current_question]  # Player keeps his score
                game_loader.loss_game_screen_setup(  # Lose-game screen is set up
                    current_display.current_questions[current_display.current_question].correctAnswer,
                    current_display.score)
                return 2  # State is changed to End-game screen

            elif clickedButtonNumber == 6:  # If the clicked button is 50/50 hint
                current_display.current_questions[current_display.current_question].fiftyFiftyUsed = True
                current_display.fifty_fifty_available = False  # Player can no longer use this hint
                current_display.current_buttons = current_display.current_questions[
                    current_display.current_question].to_buttons(True)  # Current question gets displayed again
                # but the order of answers doesn't change and two answers disappear
                current_display.current_screen.buttons = current_display.current_buttons
                return 1

            elif clickedButtonNumber == 7:  # If the clicked button is friend's help hint
                current_display.current_screen.labels.extend(  # Shown labels get extended by friend's dialog
                    current_display.current_questions[current_display.current_question].friend_help(
                        current_display.current_question))
                current_display.friend_help_available = False  # Player can no longer use this hint
                current_display.current_questions[current_display.current_question].fiftyFiftyUsed = False
                current_display.current_buttons = current_display.current_questions[
                    current_display.current_question].to_buttons(True)  # Current question gets displayed again to
                # show the new labels
                current_display.current_screen.buttons = current_display.current_buttons
                return 1

            elif clickedButtonNumber == 8:  # If the clicked button is the public help
                current_display.public_help_available = False  # Player can no longer use this hint
                current_display.current_buttons = current_display.current_questions[
                    current_display.current_question].to_buttons(True)  # Current question gets displayed again to
                # hide the hint button
                current_display.current_buttons.append(  # New not clickable button is added - a bar chart
                    current_display.current_questions[current_display.current_question].public_help(
                        current_display.current_question))
                current_display.current_screen.buttons = current_display.current_buttons
                return 1

            # 0: button where question is displayed   -1: no button clicked    9: button where bar chart is displayed
            elif clickedButtonNumber != 0 and clickedButtonNumber != -1 and clickedButtonNumber != 9 and \
                    current_display.current_buttons[clickedButtonNumber].text != "":  # If the clicked button is one
                #  with a bad answer
                current_display.score = game_loader.scores[  # Player's score gets lowered to one of the safe points
                    current_display.current_question - current_display.current_question % 5]  # Safe points are 0, 5, 10
                game_loader.loss_game_screen_setup(
                    current_display.current_questions[current_display.current_question].correctAnswer,
                    current_display.score)  # Loss screen gets loaded
                return 2  # State is changed to End-game screen

    return 1  # Else game continues


def end_game_loop():
    import current_display
    current_display.display_screen()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Alt+F4 or X button
            return -1  # Returns -1: end of the game
        elif event.type == pygame.MOUSEBUTTONUP:  # On mouse-click
            clickedButtonNumber = current_display.determine_clicked_button(pygame.mouse.get_pos())
            if clickedButtonNumber == 0:  # If clicked on empty text button, cursor gets shown and player can write
                current_display.current_buttons[0].clickedOn = True
                current_display.current_buttons[0].show_cursor()
            elif clickedButtonNumber == 1:
                current_display.current_buttons[0].clickedOn = False  # If clicked on "Cancel" button player returns
                current_display.current_buttons[0].hide_cursor()      # to main menu screen
                game_loader.first_screen_setup()
                return 0  # Back to main menu
            elif clickedButtonNumber == 2:
                current_display.current_buttons[0].clickedOn = False  # If clicked on "Confirm" button, score gets saved
                current_display.current_buttons[0].hide_cursor()      # and the highscores screen is shown to player
                if current_display.current_buttons[0].text == "":  # If the text-field is empty, player is stopped and
                    return 2   # End-game screen                   # stays in this screen to fill the field
                game_loader.write_score(current_display.current_buttons[0].text, current_display.score)
                game_loader.highscores_screen_setup()
                return 4  # Highscores screen
            elif clickedButtonNumber == -1:  # If clicked anywhere cursor in text field gets hidden
                current_display.current_buttons[0].clickedOn = False
                current_display.current_buttons[0].hide_cursor()
        elif event.type == pygame.KEYDOWN:  # If any key is pressed and player writes to the text field
            if current_display.current_buttons[0].clickedOn:
                if event.key == pygame.K_BACKSPACE:  # If it isn't one of the following keys which call operation
                                                     # functions in text field. The character gets written
                    current_display.current_buttons[0].remove_previous()
                elif event.key == pygame.K_DELETE:
                    current_display.current_buttons[0].remove_next()
                elif event.key == pygame.K_LEFT:
                    current_display.current_buttons[0].move_cursor_left()
                elif event.key == pygame.K_RIGHT:
                    current_display.current_buttons[0].move_cursor_right()
                elif event.key == pygame.K_HOME:
                    current_display.current_buttons[0].move_cursor_left(True)
                elif event.key == pygame.K_END:
                    current_display.current_buttons[0].move_cursor_right(True)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Enter (named return in pygame)
                    current_display.current_buttons[0].hide_cursor()                  # hides the cursor
                else:
                    current_display.current_buttons[0].add_char(event.unicode)
    return 2  # Else player stays here


def add_question_loop():
    import current_display
    current_display.display_screen()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Alt+F4 or X button
            return -1  # Returns -1: end of the game
        elif event.type == pygame.MOUSEBUTTONUP:  # On mouse click
            clickedButtonNumber = current_display.determine_clicked_button(pygame.mouse.get_pos())
            for i in range(len(current_display.current_buttons)):
                if i == clickedButtonNumber and i < 5:  # If clicked on text button, cursor gets shown and player can
                    current_display.current_buttons[i].clickedOn = True  # write here
                    current_display.current_buttons[i].show_cursor()
                elif i < 5:
                    current_display.current_buttons[i].clickedOn = False  # In other text buttons, cursor gets hidden
                    current_display.current_buttons[i].hide_cursor()      # and player can't write here
                elif clickedButtonNumber == 5:  # If clicked on "Cancel" button, player returns to Main menu
                    game_loader.first_screen_setup()
                    return 0
                elif clickedButtonNumber == 6:  # If clicked on "Confirm" button, question gets added
                    for i in range(5):
                        if current_display.current_buttons[i].text == "":  # Unless there is an empty text field
                            return 3  # In that case player stays in this loop, to fill them in
                    game_loader.Question(current_display.current_buttons[0].text,  # Question gets written to CSV
                                         current_display.current_buttons[1].text, (
                                             current_display.current_buttons[2].text,
                                             current_display.current_buttons[3].text,
                                             current_display.current_buttons[4].text)).write_to_csv()
                    game_loader.first_screen_setup()  # Player returns to Main menu
                    return 0  # Main menu

        elif event.type == pygame.KEYDOWN:  # If a key is pressed, player writes to currently selected text field
            for button in current_display.current_buttons:  # If it isn't one of the following keys which call operation
                                                            # functions in text field. The character gets written
                if isinstance(button, game_loader.ButtonWithText) and button.clickedOn:
                    if event.key == pygame.K_BACKSPACE:
                        button.remove_previous()
                    elif event.key == pygame.K_DELETE:
                        button.remove_next()
                    elif event.key == pygame.K_LEFT:
                        button.move_cursor_left()
                    elif event.key == pygame.K_RIGHT:
                        button.move_cursor_right()
                    elif event.key == pygame.K_HOME:
                        button.move_cursor_left(True)
                    elif event.key == pygame.K_END:
                        button.move_cursor_right(True)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Enter (return in pygame)
                        button.hide_cursor()                                              # hides the cursor
                    else:
                        button.add_char(event.unicode)

    return 3  # Else player stays here


def best_scores_loop():
    import current_display
    current_display.display_screen()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Alt+F4 or X button
            return -1  # Ends the game
        elif event.type == pygame.MOUSEBUTTONUP:  # Any click anywhere returns player to main menu
            game_loader.first_screen_setup()
            return 0
    return 4  # Else player stays here
