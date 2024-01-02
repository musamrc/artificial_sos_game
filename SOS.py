import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 100
GRID_SIZE = 5
WIDTH = HEIGHT = CELL_SIZE * GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 48
game_over = False
sos_positions = {1: [], 2: []}  # List of tuples (start_row, start_col, end_row, end_col)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))  # Additional space for player status and score
pygame.display.set_caption("SOS Game")
font = pygame.font.Font(None, FONT_SIZE)

# Game board setup
board = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
board[0][0] = board[0][GRID_SIZE-1] = board[GRID_SIZE-1][0] = board[GRID_SIZE-1][GRID_SIZE-1] = "S"

# Player setup
current_player = 1
player_symbol = None
player_scores = {1: 0, 2: 0}

# Function to draw the game board, player status, and scores
def draw_board():
    screen.fill(WHITE)
    draw_sos_lines()  # Draw the SOS lines first
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            symbol = font.render(board[row][col], True, BLACK)
            screen.blit(symbol, (col * CELL_SIZE + 20, row * CELL_SIZE + 20))
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    player_status = font.render(f"Player {current_player}'s turn ({'S' if player_symbol == 'S' else 'O'})", True, BLACK)
    screen.blit(player_status, (10, HEIGHT + 10))
    score_display = font.render(f"Scores - Player 1: {player_scores[1]} Player 2: {player_scores[2]}", True, BLACK)
    screen.blit(score_display, (10, HEIGHT + 60))
    pygame.display.flip()

def handle_move(x, y):
    global player_symbol
    row, col = y // CELL_SIZE, x // CELL_SIZE
    if board[row][col] == " " and player_symbol:
        board[row][col] = player_symbol
        sos_formed = check_sos(row, col)
        if sos_formed:
            player_scores[current_player] += sos_formed
            # Switch player after SOS
            switch_player()

# Function to handle player symbol selection
def handle_symbol_selection(key):
    global player_symbol
    if key == pygame.K_s:
        player_symbol = "S"
    elif key == pygame.K_o:
        player_symbol = "O"

# Function to switch players
def switch_player():
    global current_player, player_symbol
    current_player = 1 if current_player == 2 else 2
    player_symbol = None

def check_sos(row, col):
    global sos_positions
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Right, Down, Diagonal down-right, Diagonal up-right
    sos_count = 0

    for dr, dc in directions:
        for offset in range(-2, 1):  # Check with the current cell being at different positions in "SOS"
            seq = ''
            start_r, start_c = row + offset * dr, col + offset * dc
            end_r, end_c = start_r + 2 * dr, start_c + 2 * dc
            for i in range(3):
                r, c = start_r + i * dr, start_c + i * dc
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    seq += board[r][c]
                else:
                    break
            if seq == "SOS":
                sos_positions[current_player].append((start_r, start_c, end_r, end_c))
                sos_count += 1

    return sos_count

def draw_sos_lines():
    line_width = 5
    for player, positions in sos_positions.items():
        color = RED if player == 1 else BLUE
        for start_r, start_c, end_r, end_c in positions:
            start_x, start_y = start_c * CELL_SIZE + CELL_SIZE // 2, start_r * CELL_SIZE + CELL_SIZE // 2
            end_x, end_y = end_c * CELL_SIZE + CELL_SIZE // 2, end_r * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), line_width)


def is_board_full():
    for row in board:
        if " " in row:
            return False
    return True

def display_end_game():
    screen.fill(WHITE)
    if player_scores[1] > player_scores[2]:
        winner_text = "Player 1 Won"
    elif player_scores[2] > player_scores[1]:
        winner_text = "Player 2 Won"
    else:
        winner_text = "Draw"

    # Adjust font size based on the screen width
    end_game_font = pygame.font.Font(None, WIDTH // 15)
    score_font = pygame.font.Font(None, WIDTH // 20)

    end_game_message = end_game_font.render(winner_text, True, BLACK)
    score_message = score_font.render(f"Final Scores - Player 1: {player_scores[1]}, Player 2: {player_scores[2]}", True, BLACK)
    
    # Center the text on the screen
    end_game_rect = end_game_message.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    score_rect = score_message.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.blit(end_game_message, end_game_rect)
    screen.blit(score_message, score_rect)
    pygame.display.flip()

def main():
    global game_over
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    handle_move(*event.pos)
                    if is_board_full():
                        game_over = True
                elif event.type == pygame.KEYDOWN:
                    handle_symbol_selection(event.key)

        if game_over:
            display_end_game()
        else:
            draw_board()

        pygame.display.flip()

    pygame.time.wait(5000)  # Wait for 5 seconds before closing
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
