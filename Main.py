import pygame

from pygame.locals import QUIT
import random
import sys
import matplotlib.pyplot as plt

pygame.init()

WIDTH, HEIGHT = 300, 600
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0 , 0)
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)

grid = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ally & Izzy Tic Tac Toe Game")

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(window, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
            pygame.draw.rect(window, LINE_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Function to draw X and O
def draw_xo():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 'X':
                pygame.draw.line(window, X_COLOR, (col * CELL_SIZE, row * CELL_SIZE), ((col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE), 3)
                pygame.draw.line(window, X_COLOR, (col * CELL_SIZE, (row + 1) * CELL_SIZE), ((col + 1) * CELL_SIZE, row * CELL_SIZE), 3)
            elif grid[row][col] == 'O':
                pygame.draw.circle(window, O_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 10, 3)

def show_popup(message):
    popup_font = pygame.font.Font(None, 36)
    popup_text = popup_font.render(message, True, (0, 0, 0))
    popup_rect = popup_text.get_rect()
    popup_rect.center = (WIDTH // 2, HEIGHT // 2)
    window.blit(popup_text, popup_rect)
    pygame.display.update()
    
def check_win(player):
    for row in range(GRID_SIZE):
        if all(cell == player for cell in grid[row]):
            return True
    for col in range(GRID_SIZE):
        if all(grid[row][col] == player for row in range(GRID_SIZE)):
            return True
    if all(grid[i][i] == player for i in range(GRID_SIZE)) or all(grid[i][GRID_SIZE - i - 1] == player for i in range(GRID_SIZE)):
        return True
    return False

def check_win(computer):
    for row in range(GRID_SIZE):
        if all(cell == computer for cell in grid[row]):
            return True
    for col in range(GRID_SIZE):
        if all(grid[row][col] == computer for row in range(GRID_SIZE)):
            return True
    if all(grid[i][i] == computer for i in range(GRID_SIZE)) or all(grid[i][GRID_SIZE - i - 1] == computer for i in range(GRID_SIZE)):
        return True
    return False

# Main game loop

def check_draw():
    return all(cell != '' for row in grid for cell in row)

def computer_move():
    available_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == '']
    if available_cells:
        computer_row, computer_col = random.choice(available_cells)
        grid[computer_row][computer_col] = 'O'


running = True
game_started = False
game_over = False
player_turn = True  # True for player (X), False for computer (O)
computer_move = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_started and not game_over and player_turn:
            x, y = event.pos
            col = x // CELL_SIZE
            row = y // CELL_SIZE

            if grid[row][col] == '':
                grid[row][col] = 'X'
                player_turn = True
                if check_win('X'):
                    game_started = True
                
                if check_win('X'):
                    game_over = True
                    show_popup("Player X Wins!")
                elif all(CELL_SIZE != '' for row in grid):
                    game_over = False
                    show_popup("Its a Draw!")
            else: 
                
                if grid[row][col] == '':
                    grid[row][col] = 'O'
                computer_move = True
                if check_win('O'):
                    game_started = True
                    
                available_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == '']
                if available_cells:
                    computer_row, computer_col = random.choice(available_cells)
                    grid[computer_row][computer_col] = 'O'
                    computer_move = True
                    
                    if check_win('O'):
                        game_over = True
                        show_popup("Computer O Wins!")
                    elif all(CELL_SIZE != '' for row in grid):
                        game_over = False
                        show_popup("It's a Draw")
                    

    window.fill((0, 0, 0))

    if not game_started:
        start_button = pygame.draw.rect(window, WHITE, (50, 200, 200, 50))
        instructions_button = pygame.draw.rect(window, WHITE, (50, 300, 200, 50))
        quit_button = pygame.draw.rect(window, WHITE, (50, 400, 200, 50))

        font = pygame.font.Font(None, 36)
        start_text = font.render("Start", True, (0, 0, 0))
        instructions_text = font.render("Instructions", True, (0, 0, 0))
        quit_text = font.render("Quit", True, (0, 0, 0))

        window.blit(start_text, (120, 215))
        window.blit(instructions_text, (75, 315))
        window.blit(quit_text, (130, 415))

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if start_button.collidepoint(x, y):
                game_started = True
            elif instructions_button.collidepoint(x, y):
                instructions = ["Tic Tac Toe Instructions:", "1. Click on the grid to place your 'X'.", "2. Try to get 3 'X's in a row to win!", "3. Click 'Quit' to exit the game."]
                for i, instruction in enumerate(instructions):
                    text = font.render(instruction, True, (255, 255, 255))
                    window.blit(text, (10, 10 + i * 40))
            elif quit_button.collidepoint(x, y):
                running = False

    if game_started:
        draw_grid()
        draw_xo()

    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render("Player X Wins!", True, X_COLOR)
     #   text = font.render("Player O Wins!", True, X_COLOR)

        window.blit(text, (110, 250))
        
    

    pygame.display.update()

pygame.quit()
