
import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mondrian Tetris")

# Colors (Petite Mondrian)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

colors = [red, blue, yellow, white]

# Tetris grid
grid_size = 30
grid_width = 10
grid_height = 20
grid = [[black for _ in range(grid_width)] for _ in range(grid_height)]

# Tetromino shapes
tetrominoes = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
]

class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(colors)

    def draw(self, screen):
        for r, row in enumerate(self.shape):
            for c, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        self.color,
                        (
                            (self.x + c) * grid_size,
                            (self.y + r) * grid_size,
                            grid_size,
                            grid_size,
                        ),
                    )
                    pygame.draw.rect(
                        screen,
                        black,
                        (
                            (self.x + c) * grid_size,
                            (self.y + r) * grid_size,
                            grid_size,
                            grid_size,
                        ),
                        2,
                    )

def new_tetromino():
    return Tetromino(grid_width // 2, 0, random.choice(tetrominoes))

def is_valid_position(tetromino, grid):
    for r, row in enumerate(tetromino.shape):
        for c, cell in enumerate(row):
            if cell:
                if (
                    tetromino.x + c < 0
                    or tetromino.x + c >= grid_width
                    or tetromino.y + r >= grid_height
                    or grid[tetromino.y + r][tetromino.x + c] != black
                ):
                    return False
    return True

def lock_tetromino(tetromino, grid):
    for r, row in enumerate(tetromino.shape):
        for c, cell in enumerate(row):
            if cell:
                grid[tetromino.y + r][tetromino.x + c] = tetromino.color

def clear_lines(grid):
    lines_to_clear = []
    for r, row in enumerate(grid):
        if all(cell != black for cell in row):
            lines_to_clear.append(r)

    for r in lines_to_clear:
        del grid[r]
        grid.insert(0, [black for _ in range(grid_width)])

def draw_grid(screen, grid):
    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            if color != black:
                pygame.draw.rect(
                    screen,
                    color,
                    (c * grid_size, r * grid_size, grid_size, grid_size),
                )
                pygame.draw.rect(
                    screen,
                    black,
                    (c * grid_size, r * grid_size, grid_size, grid_size),
                    2,
                )

def main():
    clock = pygame.time.Clock()
    current_tetromino = new_tetromino()
    fall_time = 0
    fall_speed = 500  # milliseconds

    running = True
    while running:
        screen.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.x -= 1
                    if not is_valid_position(current_tetromino, grid):
                        current_tetromino.x += 1
                if event.key == pygame.K_RIGHT:
                    current_tetromino.x += 1
                    if not is_valid_position(current_tetromino, grid):
                        current_tetromino.x -= 1
                if event.key == pygame.K_DOWN:
                    current_tetromino.y += 1
                    if not is_valid_position(current_tetromino, grid):
                        current_tetromino.y -= 1
                if event.key == pygame.K_UP:
                    current_tetromino.shape = [
                        list(row) for row in zip(*current_tetromino.shape[::-1])
                    ]
                    if not is_valid_position(current_tetromino, grid):
                        current_tetromino.shape = [
                            list(row) for row in zip(*current_tetromino.shape)
                        ][::-1]
                if event.key == pygame.K_SPACE:
                    while is_valid_position(current_tetromino, grid):
                        current_tetromino.y += 1
                    current_tetromino.y -= 1
                    lock_tetromino(current_tetromino, grid)
                    clear_lines(grid)
                    current_tetromino = new_tetromino()
                    if not is_valid_position(current_tetromino, grid):
                        running = False

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time > fall_speed:
            fall_time = 0
            current_tetromino.y += 1
            if not is_valid_position(current_tetromino, grid):
                current_tetromino.y -= 1
                lock_tetromino(current_tetromino, grid)
                clear_lines(grid)
                current_tetromino = new_tetromino()
                if not is_valid_position(current_tetromino, grid):
                    running = False

        draw_grid(screen, grid)
        current_tetromino.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
