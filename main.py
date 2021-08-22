if __name__ == '__main__':
    import pygame
    import game_loader
    import game_loops

    pygame.init()
    state = 0

    game_loader.general_setup()

    while state != -1:  # Main loop of the game. Every call changes the variable state, which determines which loop
        state = game_loops.game_loop(state)  # should be used. state -1 means the end of the game
    else:
        pygame.quit()
        exit()
