import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 20, 20
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Initialize the maze grid
grid = [[0] * COLS for _ in range(ROWS)]
visited = [[False] * COLS for _ in range(ROWS)]
stack = [(0, 0)]

# Generate maze using depth-first search
while stack:
    current_cell = stack[-1]
    x, y = current_cell
    visited[y][x] = True

    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    unvisited_neighbors = [neighbor for neighbor in neighbors if 0 <= neighbor[0] < COLS and 0 <= neighbor[1] < ROWS and not visited[neighbor[1]][neighbor[0]]]

    if unvisited_neighbors:
        next_cell = random.choice(unvisited_neighbors)
        next_x, next_y = next_cell

        # Remove walls
        if next_x > x:
            grid[y][x] |= 1  # Remove right wall
            grid[next_y][next_x] |= 4  # Remove left wall
        elif next_x < x:
            grid[y][x] |= 4  # Remove left wall
            grid[next_y][next_x] |= 1  # Remove right wall
        elif next_y > y:
            grid[y][x] |= 2  # Remove bottom wall
            grid[next_y][next_x] |= 8  # Remove top wall
        elif next_y < y:
            grid[y][x] |= 8  # Remove top wall
            grid[next_y][next_x] |= 2  # Remove bottom wall

        stack.append(next_cell)
    else:
        stack.pop()

# Solve the maze using depth-first search
def dfs_solve_maze(x, y, path):
    if x == COLS - 1 and y == ROWS - 1:
        return True
    
    if grid[y][x] & 1 and not (x + 1, y) in path and dfs_solve_maze(x + 1, y, path + [(x, y)]):
        return True
    if grid[y][x] & 2 and not (x, y + 1) in path and dfs_solve_maze(x, y + 1, path + [(x, y)]):
        return True
    if grid[y][x] & 4 and not (x - 1, y) in path and dfs_solve_maze(x - 1, y, path + [(x, y)]):
        return True
    if grid[y][x] & 8 and not (x, y - 1) in path and dfs_solve_maze(x, y - 1, path + [(x, y)]):
        return True

    return False

solved_path = []
dfs_solve_maze(0, 0, [])
solved_path.append((0, 0))

# Animate the solving process
solving_index = 1

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Draw maze
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] & 1:
                pygame.draw.line(screen, BLACK, (x * CELL_WIDTH + CELL_WIDTH, y * CELL_HEIGHT), (x * CELL_WIDTH + CELL_WIDTH, y * CELL_HEIGHT + CELL_HEIGHT), 2)
            if grid[y][x] & 2:
                pygame.draw.line(screen, BLACK, (x * CELL_WIDTH, y * CELL_HEIGHT + CELL_HEIGHT), (x * CELL_WIDTH + CELL_WIDTH, y * CELL_HEIGHT + CELL_HEIGHT), 2)
            if grid[y][x] & 4:
                pygame.draw.line(screen, BLACK, (x * CELL_WIDTH, y * CELL_HEIGHT), (x * CELL_WIDTH, y * CELL_HEIGHT + CELL_HEIGHT), 2)
            if grid[y][x] & 8:
                pygame.draw.line(screen, BLACK, (x * CELL_WIDTH, y * CELL_HEIGHT), (x * CELL_WIDTH + CELL_WIDTH, y * CELL_HEIGHT), 2)

    # Draw solved path
    for i in range(min(len(solved_path), solving_index) - 1):
        pygame.draw.line(screen, (0, 255, 0), (solved_path[i][0] * CELL_WIDTH + CELL_WIDTH // 2, solved_path[i][1] * CELL_HEIGHT + CELL_HEIGHT // 2), (solved_path[i+1][0] * CELL_WIDTH + CELL_WIDTH // 2, solved_path[i+1][1] * CELL_HEIGHT + CELL_HEIGHT // 2), 4)

    if solving_index < len(solved_path):
        solving_index += 1

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
