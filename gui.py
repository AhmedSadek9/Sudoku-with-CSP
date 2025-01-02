import pygame
import sys
import main

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1050, 742
BUTTON_WIDTH, BUTTON_HEIGHT = 350, 100
BUTTON_GAP = 100

# Colors with rgb
WHITE = (255, 255, 255)
LIGHTGREY = (170, 170, 170)
GRAY = (233, 228, 216)
DARKGREY = (36, 18, 63)
DARKER_GREY = (35, 35, 35)
PURPLE = (125, 84, 222)
BLACK = (0, 0, 0)
RED = (230, 30, 30)
DARKRED = (150, 0, 0)
GREEN = (30, 230, 30)
DARKGREEN = (0, 125, 0)
BLUE = (30, 30, 122)
CYAN = (30, 230, 230)
GOLD = (225, 185, 0)
DARKGOLD = (165, 125, 0)
YELLOW = (255, 255, 0)
PERIWINKLE = (183, 195, 243)

# Create the main window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")

# Load background image
background_image = pygame.image.load("sudoko/background_image.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
# Fonts
font = pygame.font.SysFont(None, 36)

# Buttons
button_font = pygame.font.SysFont(None, 24)

buttons = [
    pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, 100, BUTTON_WIDTH, BUTTON_HEIGHT),
    pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT),
    pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, 500, BUTTON_WIDTH, BUTTON_HEIGHT)
]

button_texts = [
    "Mode 1: AI Generate And Solve",
    "Mode 2: User Generate And AI Solve",
    "Mode 3: User Generate And User Solve"
]


def draw_sudoku_board(window, board):
    cell_size = 70
    cell_margin = 10
    # subgrid_size = 3 * (cell_size + cell_margin) + 3
    board_size = 9 * cell_size + 10 * cell_margin
    board_start_x = 15
    board_start_y = 15

    # Define a larger font size for the numbers
    number_font = pygame.font.SysFont(None, 40)

    for i in range(9):
        for j in range(9):
            cell_x = board_start_x + j * (cell_size + cell_margin)
            cell_y = board_start_y + i * (cell_size + cell_margin)
            pygame.draw.rect(window, WHITE, (cell_x, cell_y, cell_size, cell_size), border_radius=10)

            if board[i][j] != 0:
                # Render the number with the larger font size
                text_surface = number_font.render(str(board[i][j]), True, PURPLE)
                text_rect = text_surface.get_rect(center=(cell_x + cell_size / 2, cell_y + cell_size / 2))
                window.blit(text_surface, text_rect)
            # if i % 3 == 0 and j % 3 == 0:
            # pygame.draw.rect(window, PERIWINKLE, (cell_x - cell_margin +3, cell_y - cell_margin+3, subgrid_size, subgrid_si

def mode_1_window():
    # Create a new window for Mode 1
    mode_1_window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Mode 1")
    #unsolvable_sound = pygame.mixer.Sound('sudoko/1.wav')  # Replace 'unsolvable_sound.wav' with your sound file


    # Generate a random Sudoku puzzle
    puzzle = main.generate_random_puzzle()

    # Main loop for Mode 1 window
    mode_1_running = True
    error_message = None  # Initialize error message to None
    while mode_1_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mode_1_running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if solve button is clicked
                if 790 <= event.pos[0] <= 990 and 600 <= event.pos[1] <= 650:
                    # Solve the puzzle
                    st = main.time.time()
                    solved_puzzle = main.solve_sudoku(puzzle)
                    ed = main.time.time()
                    if solved_puzzle is not None:
                        # Calculate and print the elapsed time
                        elapsed_time = ed - st
                        print(f"The code took {elapsed_time:.5f} seconds to execute.")
                        # Update the Sudoku board if the puzzle is solvable
                        puzzle = solved_puzzle
                        error_message = None  # Clear any previous error message
                    else:
                        # Set error message if the puzzle is unsolvable
                        error_message = "The puzzle is unsolvable."
                        #unsolvable_sound.play()

                # Check if regenerate button is clicked
                elif 790 <= event.pos[0] <= 990 and 675 <= event.pos[1] <= 725:
                    # Regenerate the puzzle
                    puzzle = main.generate_random_puzzle()
                    error_message = None  # Clear any previous error message
                # Check if back button is clicked
                elif 950 <= event.pos[0] <= 1000 and 10 <= event.pos[1] <= 30:
                    # Exit Mode 1 and return to main window
                    mode_1_running = False

        # Draw the Sudoku board
        mode_1_window.fill(DARKGREY)
        draw_sudoku_board(mode_1_window, puzzle)
        # Draw error message if present
        if error_message:
            error_font = pygame.font.SysFont(None, 36)
            error_text = error_font.render(error_message, True, RED)
            error_rect = error_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            mode_1_window.blit(error_text, error_rect)

        # Draw buttons
        pygame.draw.rect(mode_1_window, PURPLE, (790, 600 - 5, 200, 50), border_radius=5)
        pygame.draw.rect(mode_1_window, PURPLE, (790, 675 - 5, 200, 50), border_radius=5)
        pygame.draw.rect(mode_1_window, PERIWINKLE, (950, 10, 50, 20), border_radius=5)  # Back button

        # Add text to buttons
        button_font = pygame.font.SysFont(None, 24)
        regenerate_text = button_font.render("Solve Board", True, WHITE)
        solve_text = button_font.render("Regenerate New", True, WHITE)
        mode_1_window.blit(regenerate_text, (835, 610))
        mode_1_window.blit(solve_text, (830, 685))
        back_text = button_font.render("Back", True, DARKGREY)
        mode_1_window.blit(back_text, (955, 12))

        # Update the display
        pygame.display.flip()


def mode_2_window():
    # Create a new window for Mode 2
    mode_2_window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Mode 2")
    unsolvable_sound = pygame.mixer.Sound('sudoko/1.wav')  # Replace 'unsolvable_sound.wav' with your sound file


    # Initialize an empty Sudoku puzzle
    puzzle = [[0 for _ in range(9)] for _ in range(9)]

    # Track the selected cell position
    selected_cell = None

    # Main loop for Mode 2 window
    mode_2_running = True
    error_message = None  # Initialize error message to None
    while mode_2_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mode_2_running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if back button is clicked
                if 950 <= event.pos[0] <= 1000 and 10 <= event.pos[1] <= 30:
                    # Exit Mode 2 and return to the main window
                    mode_2_running = False
                elif 790 <= event.pos[0] <= 990 and 670 <= event.pos[1] <= 720:
                    # Check if the puzzle is valid
                    if main.is_valid_sudoku(puzzle):
                        # Solve the puzzle when "Solve Board" button is clicked
                        st = main.time.time()
                        solved_puzzle = main.solve_sudoku(puzzle)
                        ed = main.time.time()
                        if solved_puzzle is not None:
                            # Calculate and print the elapsed time
                            elapsed_time = ed - st
                            print(f"The code took {elapsed_time:.5f} seconds to execute.")
                            puzzle = solved_puzzle
                            error_message = None  # Clear any previous error message
                        else:
                            error_message = "The puzzle is unsolvable."
                            unsolvable_sound.play()

                    else:
                        error_message = "Invalid Sudoku Input, Please Check Game Constrains"
                elif 790 <= event.pos[0] <= 990 and 600 <= event.pos[1] <= 650:
                    # Reset the puzzle when "Reset Board" button is clicked
                    puzzle = [[0 for _ in range(9)] for _ in range(9)]
                    error_message = None  # Clear any previous error message
                else:
                    # Get the clicked cell position
                    cell_x = (event.pos[0] - 10) // 80  # Calculate cell column based on click position
                    cell_y = (event.pos[1] - 10) // 80  # Calculate cell row based on click position
                    if 0 <= cell_x < 9 and 0 <= cell_y < 9:
                        # Highlight the selected cell
                        selected_cell = (cell_x, cell_y)

            elif event.type == pygame.KEYDOWN and selected_cell is not None:
                # Check if a number key (1-9) is pressed
                if pygame.K_1 <= event.key <= pygame.K_9:
                    # Update the value of the selected cell
                    puzzle[selected_cell[1]][selected_cell[0]] = int(event.unicode)
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    # Clear the value of the selected cell
                    puzzle[selected_cell[1]][selected_cell[0]] = 0

        # Draw the Sudoku board
        mode_2_window.fill(DARKGREY)
        draw_sudoku_board(mode_2_window, puzzle)

        # Draw yellow highlight for the selected cell
        if selected_cell is not None:
            cell_x, cell_y = selected_cell
            pygame.draw.rect(mode_2_window, YELLOW, (cell_x * 80 + 12, cell_y * 80 + 12, 73, 73), 5, border_radius=10)

        # Draw error message if present
        if error_message:
            error_font = pygame.font.SysFont(None, 36)
            error_text = error_font.render(error_message, True, RED)
            error_rect = error_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            mode_2_window.blit(error_text, error_rect)

        # Draw buttons
        pygame.draw.rect(mode_2_window, PURPLE, (790, 670, 200, 50), border_radius=5)
        pygame.draw.rect(mode_2_window, PURPLE, (790, 600, 200, 50), border_radius=5)
        pygame.draw.rect(mode_2_window, PERIWINKLE, (950, 10, 50, 20), border_radius=5)  # Back button

        # Add text to buttons
        button_font = pygame.font.SysFont(None, 24)
        solve_text = button_font.render("Solve Board", True, WHITE)
        mode_2_window.blit(solve_text, (840, 685))
        reset_text = button_font.render("Reset Board", True, WHITE)
        mode_2_window.blit(reset_text, (840, 615))
        back_text = button_font.render("Back", True, DARKGREY)
        mode_2_window.blit(back_text, (955, 12))

        # Update the display
        pygame.display.flip()

    # Once the user exits the Mode 2 window, return the user input Sudoku puzzle
    return puzzle


def mode_3_window():
    # Create a new window for Mode 2
    mode_2_window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Mode 3")
    unsolvable_sound = pygame.mixer.Sound('sudoko/1.wav')  # Replace 'unsolvable_sound.wav' with your sound file


    # Initialize an empty Sudoku puzzle
    puzzle = [[0 for _ in range(9)] for _ in range(9)]

    # Track the selected cell position
    selected_cell = None

    # Initialize solved puzzle and user input grid
    solved_puzzle = None
    user_input_grid = [[0 for _ in range(9)] for _ in range(9)]

    # Main loop for Mode 2 window
    mode_2_running = True
    error_message = None  # Initialize error message to None
    while mode_2_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mode_2_running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if back button is clicked
                if 950 <= event.pos[0] <= 1000 and 10 <= event.pos[1] <= 30:
                    # Exit Mode 2 and return to the main window
                    mode_2_running = False
                elif 790 <= event.pos[0] <= 990 and 670 <= event.pos[1] <= 720:
                    # Solve the puzzle and store the solution
                    if solved_puzzle is None:
                        solved_puzzle = main.solve_sudoku(user_input_grid)
                        print(solved_puzzle)
                elif 790 <= event.pos[0] <= 990 and 600 <= event.pos[1] <= 650:
                    # Reset the puzzle when "Reset Board" button is clicked
                    puzzle = [[0 for _ in range(9)] for _ in range(9)]
                    user_input_grid = [[0 for _ in range(9)] for _ in range(9)]
                    error_message = None  # Clear any previous error message
                else:
                    # Get the clicked cell position
                    cell_x = (event.pos[0] - 10) // 80  # Calculate cell column based on click position
                    cell_y = (event.pos[1] - 10) // 80  # Calculate cell row based on click position
                    if 0 <= cell_x < 9 and 0 <= cell_y < 9:
                        # Highlight the selected cell
                        selected_cell = (cell_x, cell_y)

            elif event.type == pygame.KEYDOWN and selected_cell is not None:
                # Check if a number key (1-9) is pressed
                if pygame.K_1 <= event.key <= pygame.K_9:
                    # Update the value of the selected cell in user input grid
                    user_input_grid[selected_cell[1]][selected_cell[0]] = int(event.unicode)
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    # Clear the value of the selected cell in user input grid
                    user_input_grid[selected_cell[1]][selected_cell[0]] = 0

        # Draw the Sudoku board with user input
        mode_2_window.fill(DARKGREY)
        draw_sudoku_board(mode_2_window, user_input_grid)

        # Draw yellow highlight for the selected cell
        if selected_cell is not None:
            cell_x, cell_y = selected_cell
            pygame.draw.rect(mode_2_window, YELLOW, (cell_x * 80 + 12, cell_y * 80 + 12, 72, 72), 5, border_radius=10)

        # Compare user input with solver's solution in real-time
        if solved_puzzle is not None:
            for y in range(9):
                for x in range(9):
                    if user_input_grid[y][x] != 0 and user_input_grid[y][x] != solved_puzzle[y][x]:
                        # Draw red border for incorrect user input
                        pygame.draw.rect(mode_2_window, RED, (x * 80 + 12, y * 80 + 12, 72, 72), 5, border_radius=10)
                        unsolvable_sound.play()


        # Draw buttons
        pygame.draw.rect(mode_2_window, PURPLE, (790, 670, 200, 50), border_radius=5)
        pygame.draw.rect(mode_2_window, PURPLE, (790, 600, 200, 50), border_radius=5)
        pygame.draw.rect(mode_2_window, PERIWINKLE, (950, 10, 50, 20), border_radius=5)  # Back button

        # Add text to buttons
        button_font = pygame.font.SysFont(None, 24)
        solve_text = button_font.render("Solve Board", True, WHITE)
        mode_2_window.blit(solve_text, (840, 685))
        reset_text = button_font.render("Reset Board", True, WHITE)
        mode_2_window.blit(reset_text, (840, 615))
        back_text = button_font.render("Back", True, DARKGREY)
        mode_2_window.blit(back_text, (955, 12))

        # Update the display
        pygame.display.flip()

    # Once the user exits the Mode 2 window, return the user input Sudoku puzzle
    return user_input_grid

# Main loop
mode_1_active = False  # Flag to track if Mode 1 window is active
mode_2_active = False  # Flag to track if Mode 2 window is active
mode_3_active = False  # Flag to track if Mode 3 window is active
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if any button was clicked
            for i, button in enumerate(buttons):
                if button.collidepoint(event.pos):
                    if i == 0:  # Mode 1 button clicked
                        mode_1_active = True
                        mode_2_active = False
                        mode_3_active = False
                    elif i == 1:  # Mode 2 button clicked
                        mode_2_active = True
                        mode_1_active = False
                        mode_3_active = False
                    elif i == 2:  # Mode 3 button clicked
                        mode_3_active = True
                        mode_1_active = False
                        mode_2_active = False

    # Draw background and buttons
    window.blit(background_image, (0, 0))
    for i, button in enumerate(buttons):
        pygame.draw.rect(window, GRAY, button, border_radius=10)
        text = button_font.render(button_texts[i], True, BLACK)
        text_rect = text.get_rect(center=button.center)
        window.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

    # If Mode 1 window is active, switch to Mode 1 window
    if mode_1_active:
        mode_1_active = False  # Reset the flag
        mode_1_window()  # Call the Mode 1 window function

    # If Mode 2 window is active, switch to Mode 2 window
    if mode_2_active:
        mode_2_active = False  # Reset the flag
        mode_2_window()  # Call the Mode 2 window function

    # If Mode 3 window is active, switch to Mode 3 window
    if mode_3_active:
        mode_3_active = False  # Reset the flag
        mode_3_window()  # Call the Mode 3 window function