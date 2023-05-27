# Import necessary libraries
import sys
import numpy as np
import pygame
import math

# Initialize pygame and its font module
pygame.init()
pygame.font.init()

# Define constants
ROWS, COLS = 6, 7  # Dimensions of the game board
BLUE, WHITE, BLACK, RED, YELLOW = (0, 0, 255), (255, 255, 255), (0, 0, 0), (255, 0, 0), (255, 255, 0)  # Color definitions
RADIUS = 45  # Radius of game piece
MARGIN = 20  # Margin between game board and window
SQUARE_SIZE = 100  # Size of a square on the game board
SCREEN_SIZE = (COLS * SQUARE_SIZE + 2 * MARGIN, (ROWS + 1) * SQUARE_SIZE + 2 * MARGIN)  # Dimensions of the game window
FONT_NAME = "monospace"  # Font name for text rendering
FONT_SIZE = 75  # Font size for main text
MEDIUM_FONT_SIZE = 50 # Font size for medium font
MEDIUM_FONT = pygame.font.SysFont(FONT_NAME, MEDIUM_FONT_SIZE) # Mediu, font for text rendering
SMALL_FONT_SIZE = 30  # Font size for small text
SMALL_FONT = pygame.font.SysFont(FONT_NAME, SMALL_FONT_SIZE)  # Small font for text rendering

# Initialize pygame
pygame.init()
FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)  # Main font for text rendering
SCREEN = pygame.display.set_mode(SCREEN_SIZE)  # Game window

# A function that creates the game board in its initial state
def create_game_board():
    """
    Creates and returns a new game board.

    Parameters
    ----------
    None

    Returns
    -------
    numpy.ndarray: A 2D array of zeros representing the game board.
    """
    return np.zeros((ROWS, COLS))

# Function that checks the validity of a given position
def is_column_valid(board, col):
    """
    Checks if a given column in the board is a valid position to place a piece.

    Parameters
    ----------
    board : TYPE: numpy.ndarray
        DESCRIPTION: The game board.
    col : TYPE: int
        DESCRIPTION: The column to check.

    Returns
    -------
    bool: True if the column is valid (topmost row in the column is zero), False otherwise.
    """
    return board[ROWS - 1][col] == 0

# Function to find the next open row on the board
def find_open_row(board, col):
    """
    Finds the next open row in a given column of the board.

    Parameters
    ----------
    board : TYPE: numpy.ndarray
        DESCRIPTION: The game board.
    col : TYPE: int
        DESCRIPTION: The column to check.

    Returns
    -------
    int: The index of the next open row in the column. If the column is full, this function will return None.
    """
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

# Function to place the next piece on the board
def drop_piece(board, row, col, piece):
    """
    Places a piece at the specified position on the board.

    Parameters
    ----------
    board : TYPE: numpy.ndarray
        DESCRIPTION: The game board.
    row : TYPE: int
        DESCRIPTION: The row index.
    col : TYPE: int
        DESCRIPTION: The column index.
    piece : TYPE: int
        DESCRIPTION: The game piece to be placed. In this game, 1 represents a red piece and 2 represents a yellow piece.

    Returns
    -------
    None. Modifies the given board in-place.
    """
    board[row][col] = piece

# Draw the board game on the screen using the pygame library
def draw_board(board):
    """
    Draws the game board on the screen.

    Parameters
    ----------
    board : TYPE: numpy.ndarray
        DESCRIPTION: The game board.

    Returns
    -------
    None. Fills the entire window with white color, then draws the squares and circles that make up the game board.
    """
    # Fill the entire window (including margins) with white
    SCREEN.fill(WHITE)

    # Draw the game board starting from (MARGIN, MARGIN)
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(SCREEN, BLUE, 
                             (MARGIN + c * SQUARE_SIZE, 
                              MARGIN + r * SQUARE_SIZE + SQUARE_SIZE, 
                              SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(SCREEN, WHITE,
                               (MARGIN + int(c * SQUARE_SIZE + SQUARE_SIZE / 2), 
                                MARGIN + int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), 
                               RADIUS)

    # Draw the pieces starting from (MARGIN, MARGIN)
    for c in range(COLS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(SCREEN, RED, 
                                   (MARGIN + int(c * SQUARE_SIZE + SQUARE_SIZE / 2), 
                                    SCREEN_SIZE[1] - int(r * SQUARE_SIZE + SQUARE_SIZE / 2) - MARGIN), 
                                   RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(SCREEN, YELLOW, 
                                   (MARGIN + int(c * SQUARE_SIZE + SQUARE_SIZE / 2), 
                                    SCREEN_SIZE[1] - int(r * SQUARE_SIZE + SQUARE_SIZE / 2) - MARGIN), 
                                   RADIUS)
    pygame.display.update()


# Checks if a move would win the game by investigating if there is 4 in a row in all rows columns and diagonals
def is_winning_move(board, piece):
    """
    Checks if the last move with the given piece is a winning move.

    Parameters
    ----------
    board : TYPE: numpy.ndarray
        DESCRIPTION: The game board.
    piece : TYPE: int
        DESCRIPTION: The piece to check.

    Returns
    -------
    bool: True if the piece has a winning position (four pieces in a row horizontally, vertically, or diagonally), False otherwise.
    """
    # Horizontal check
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Positive diagonal check
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Negative diagonal check
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# Draws the start screen for the game
def draw_start_screen():
    """
    Draws the start screen for the game.

    Parameters
    ----------
    None.

    Returns
    -------
    None. Creates and positions the title of the game and a "Start" button on the screen and updates the screen.
    """
    SCREEN.fill(WHITE)
    start_font = pygame.font.SysFont(FONT_NAME, 100)
    start_text = start_font.render("Connect Four", True, BLACK)
    start_rect = start_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3))
    SCREEN.blit(start_text, start_rect)

    # Draw "Start" button
    button_font = pygame.font.SysFont(FONT_NAME, 50)
    button_text = button_font.render("Start", True, BLACK)
    button_rect = pygame.Rect(SCREEN_SIZE[0] // 2 - 100, SCREEN_SIZE[1] // 2, 200, 100)
    pygame.draw.rect(SCREEN, BLUE, button_rect)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    SCREEN.blit(button_text, button_text_rect)

    pygame.display.flip()

# Function that is called when someone wins the game
def game_over_message(player):
    """
    Displays a message when the game is over.

    Parameters
    ----------
    player : TYPE: int
        DESCRIPTION: The winning player.

    Returns
    -------
    None. Creates and positions a winning message based on the player who won, updates the screen and waits for 3000 milliseconds.
    """
    SCREEN.fill(WHITE)
    label = FONT.render(f"Player {player} wins!!", 1, RED if player == 1 else YELLOW)
    SCREEN.blit(label, (SCREEN_SIZE[0] // 2 - label.get_width() // 2, SCREEN_SIZE[1] // 2 - label.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(3000)

# Function that is called when the game is a draw
def game_over_draw():
    """
    Displays a message when the game is over.
    
    Returns
    -------
    None. Creates and positions a draw message based on if the game is a draw, updates the screen and waits for 3000 milliseconds.
    """
    SCREEN.fill(WHITE)
    label = MEDIUM_FONT.render("The game ends in a draw!", 1, RED)
    SCREEN.blit(label, (SCREEN_SIZE[0] // 2 - label.get_width() // 2, SCREEN_SIZE[1] // 2 - label.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(3000)

# Function that draws the end screen after the game is finished
def draw_end_screen(player, score):
    """
    Draws the end screen for the game.

    Parameters
    ----------
    player : TYPE: int
        DESCRIPTION: The winning player.
    score : TYPE: list
        DESCRIPTION: A list of two integers representing the scores of the two players.

    Returns
    -------
    None. Creates and positions the winning message, scores of both players, and "Play Again" and "Quit" buttons on the screen, and updates the screen.
    """
    # If condition to print the end game message and score based on who won (or a draw)
    if player == 3:
        SCREEN.fill(WHITE)
        label = MEDIUM_FONT.render("The game ends in a draw!!".format(player), 1, BLACK)
        score_label = SMALL_FONT.render("Player 1: {} - Player 2: {}".format(score[0], score[1]), 1, BLACK)
        play_again_label = SMALL_FONT.render("Play Again", 1, WHITE)
        quit_label = SMALL_FONT.render("Quit", 1, WHITE)
    else:
            SCREEN.fill(WHITE)
            label = FONT.render("Player {} wins!!".format(player), 1, RED if player == 1 else YELLOW)
            score_label = SMALL_FONT.render("Player 1: {} - Player 2: {}".format(score[0], score[1]), 1, BLACK)
            play_again_label = SMALL_FONT.render("Play Again", 1, WHITE)
            quit_label = SMALL_FONT.render("Quit", 1, WHITE)

    SCREEN.blit(label, (SCREEN_SIZE[0] // 2 - label.get_width() // 2, SCREEN_SIZE[1] // 2 - 200))
    SCREEN.blit(score_label, (SCREEN_SIZE[0] // 2 - score_label.get_width() // 2, SCREEN_SIZE[1] // 2 - 100))

    button_width = 200
    button_height = 100
    gap_between_buttons = 50

    # Calculate positions for buttons
    play_again_button_x = SCREEN_SIZE[0] // 2 - button_width - gap_between_buttons // 2
    quit_button_x = SCREEN_SIZE[0] // 2 + gap_between_buttons // 2
    button_y = SCREEN_SIZE[1] // 2 + 100

    play_again_rect = pygame.draw.rect(SCREEN, BLUE, (play_again_button_x, button_y, button_width, button_height))
    SCREEN.blit(play_again_label, (play_again_rect.centerx - play_again_label.get_width() // 2, play_again_rect.centery - play_again_label.get_height() // 2))

    quit_rect = pygame.draw.rect(SCREEN, BLUE, (quit_button_x, button_y, button_width, button_height))
    SCREEN.blit(quit_label, (quit_rect.centerx - quit_label.get_width() // 2, quit_rect.centery - quit_label.get_height() // 2))

    pygame.display.update()
    
    
# Function that initializes the main game loop
def main():
    """
    Initiates the main game loop.

    Parameters
    ----------
    None.

    Returns
    -------
    None. Handles the flow of the game including the start screen, game loop, and end screen. Handles events like mouse clicks and movement, checks if a move is valid, checks if a player has won, and restarts or exits the game.
    """

    while True:  # Main game loop
        score = [0, 0]  # Score for Player 1 and 2, reset each time the game is started

        board = create_game_board()
        game_over = False
        max_moves = ROWS * COLS # Maximum moves for the game
        total_moves = 0 # Counter for total moves made 
        turn = 0

        # Start screen
        start_screen = True
        while start_screen:
            draw_start_screen()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if SCREEN_SIZE[0] // 2 - 100 < mouse_pos[0] < SCREEN_SIZE[0] // 2 + 100 and SCREEN_SIZE[1] // 2 < mouse_pos[1] < SCREEN_SIZE[1] // 2 + 100:
                        start_screen = False
                        draw_board(board)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        while not game_over:  # Game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(SCREEN, BLACK, (0, 0, SCREEN_SIZE[0], SQUARE_SIZE))
                    pos_x = event.pos[0]
                    color = RED if turn == 0 else YELLOW
                    pygame.draw.circle(SCREEN, color, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(SCREEN, BLACK, (0, 0, SCREEN_SIZE[0], SQUARE_SIZE))
                    pos_x = event.pos[0]
                    if pos_x >= SCREEN_SIZE[0] -55:
                        pos_x = SCREEN_SIZE[0] -55
                    col = int(math.floor(pos_x / SQUARE_SIZE))

                    if is_column_valid(board, col):
                        row = find_open_row(board, col)
                        drop_piece(board, row, col, turn + 1)

                        if is_winning_move(board, turn + 1):
                            winning_player = turn + 1
                            game_over_message(winning_player)
                            game_over = True
                            score[turn] += 1
                        turn = (turn + 1) % 2 # Move to next turn only when piece is successfully dropped
                        total_moves += 1
                        
                        # Check if the total_moves reached the maximum amount of moves, call the game a draw
                        if total_moves == max_moves:
                            game_over = True
                            game_over_draw()
                            score[0] += 1
                            score[1] += 1
                            winning_player = 3
                    else:
                        # If column is not valid, display an error message
                        error_label = SMALL_FONT.render("Column is full. Choose a different column.", True, BLACK)
                        SCREEN.blit(error_label, (SCREEN_SIZE[0] // 2 - error_label.get_width() // 2, SCREEN_SIZE[1] - error_label.get_height() - 20))
                        pygame.display.update()
                        pygame.time.wait(2000)

                    draw_board(board)

            if game_over:
                draw_end_screen(winning_player, score)
                total_moves = 0

            # End game loop
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if SCREEN_SIZE[0] // 3 - 50 < mouse_pos[0] < SCREEN_SIZE[0] // 3 + 150 and SCREEN_SIZE[1] // 2 + 100 < mouse_pos[1] < SCREEN_SIZE[1] // 2 + 150:  # Play again
                            game_over = False
                            # Refresh the board here
                            board = create_game_board()
                            draw_board(board)
                        elif SCREEN_SIZE[0] // 2 < mouse_pos[0] < SCREEN_SIZE[0] // 2 + 200 and SCREEN_SIZE[1] // 2 + 100 < mouse_pos[1] < SCREEN_SIZE[1] // 2 + 150:  # Quit
                            pygame.quit()
                            sys.exit()
              