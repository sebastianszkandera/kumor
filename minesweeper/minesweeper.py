import json
import random
import time
import pygame
import pygame.locals as pl


def game():
    pygame.init()  # Initialize Pygame
    window = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)
    grid_size = 10
    cell_size = 40
    mines_count = 15
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    RED = (255, 0, 0)
    
    # Initialize game grid
    # -1 = mine, 0-8 = number of adjacent mines, 9 = revealed, 10 = flagged
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    revealed = [[False for _ in range(grid_size)] for _ in range(grid_size)]
    flagged = [[False for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Place mines randomly
    mines_placed = 0
    while mines_placed < mines_count:
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        if grid[y][x] != -1:
            grid[y][x] = -1
            mines_placed += 1
    
    # Calculate numbers for adjacent mines
    for y in range(grid_size):
        for x in range(grid_size):
            if grid[y][x] != -1:
                count = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < grid_size and 0 <= nx < grid_size and grid[ny][nx] == -1:
                            count += 1
                grid[y][x] = count
    
    def reveal_cell(x, y):
        if not (0 <= x < grid_size and 0 <= y < grid_size) or revealed[y][x] or flagged[y][x]:
            return
        
        revealed[y][x] = True
        
        if grid[y][x] == 0:  # Empty cell, reveal neighbors
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    reveal_cell(x + dx, y + dy)
    
    def draw_grid():
        window.fill(WHITE)
        
        for y in range(grid_size):
            for x in range(grid_size):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                
                if revealed[y][x]:
                    pygame.draw.rect(window, GRAY, rect)
                    pygame.draw.rect(window, DARK_GRAY, rect, 1)
                    
                    if grid[y][x] == -1:  # Mine
                        pygame.draw.circle(window, BLACK, rect.center, cell_size // 4)
                    elif grid[y][x] > 0:  # Number
                        text = font.render(str(grid[y][x]), True, BLACK)
                        text_rect = text.get_rect(center=rect.center)
                        window.blit(text, text_rect)
                else:
                    pygame.draw.rect(window, GRAY, rect)
                    pygame.draw.rect(window, DARK_GRAY, rect, 1)
                    
                    if flagged[y][x]:
                        # Draw flag (simple triangle)
                        flag_points = [
                            (rect.left + 5, rect.top + 5),
                            (rect.left + 5, rect.bottom - 5),
                            (rect.right - 5, rect.centery)
                        ]
                        pygame.draw.polygon(window, RED, flag_points)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Determine which button was clicked
                grid_x = mouse_x // cell_size
                grid_y = mouse_y // cell_size
                
                if not (0 <= grid_x < grid_size and 0 <= grid_y < grid_size):
                    continue
                
                if event.button == 1:  # Left mouse button - reveal cell
                    if not flagged[grid_y][grid_x]:
                        reveal_cell(grid_x, grid_y)
                
                elif event.button == 3:  # Right mouse button - flag/unflag
                    if not revealed[grid_y][grid_x]:
                        flagged[grid_y][grid_x] = not flagged[grid_y][grid_x]
        
        # Draw the game
        draw_grid()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    game()