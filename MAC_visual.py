import pygame #this is the library used to create the interface for the game, It provides modules and functions to handle computer graphics, sound, and user input.
import sys
import numpy as np
import pandas as pd
import time

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver Visualizer")

# Initialize the font
font = pygame.font.Font(None, 36)

def draw_grid():
    # Draw grid lines
    for i in range(1, GRID_SIZE):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 3)
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 3)
        else:
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))

def draw_numbers(grid):
    # Draw numbers on the grid
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] != 0:
                num = font.render(str(grid[i][j]), True, BLACK)
                screen.blit(num, (j * CELL_SIZE + 20, i * CELL_SIZE + 20))

def clear_cell(row, col):
    pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    draw_grid()  # Redraw grid lines

def is_safe(puzzle, row, col, num):
    # Check if the number is not already present in the row, column, and the current 3x3 square
    return (
        all(num != puzzle[row][i] for i in range(GRID_SIZE)) and
        all(num != puzzle[i][col] for i in range(GRID_SIZE)) and
        all(num != puzzle[row - row % 3 + i][col - col % 3 + j] for i in range(3) for j in range(3))
    )

def apply_arc_consistency(puzzle, row, col, num):
    # Apply arc consistency in the row
    for i in range(GRID_SIZE):
        if i != col:
            puzzle[row][i] = np.delete(puzzle[row][i], np.where(puzzle[row][i] == num))

    # Apply arc consistency in the column
    for i in range(GRID_SIZE):
        if i != row:
            puzzle[i][col] = np.delete(puzzle[i][col], np.where(puzzle[i][col] == num))

    # Apply arc consistency in the square
    square_row, square_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(square_row, square_row + 3):
        for j in range(square_col, square_col + 3):
            if i != row or j != col:
                puzzle[i][j] = np.delete(puzzle[i][j], np.where(puzzle[i][j] == num))

def solve_sudoku_with_arc_consistency(puzzle):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if puzzle[i][j] == 0:
                for num in range(1, 10):
                    if is_safe(puzzle, i, j, num):
                        pygame.time.delay(100)
                        draw_numbers(puzzle)
                        pygame.display.update()

                        clear_cell(i, j)  # Clear the cell
                        pygame.display.update()

                        puzzle[i][j] = num
                        apply_arc_consistency(puzzle, i, j, num)
                        draw_numbers(puzzle)
                        pygame.display.update()

                        if solve_sudoku_with_arc_consistency(puzzle):
                            return True

                        pygame.time.delay(100)
                        puzzle[i][j] = 0
                        draw_numbers(puzzle)
                        pygame.display.update()

                return False

    return True

def main():
    # Read Sudoku data
    sudoku_df = pd.DataFrame(pd.read_csv('sudoku.csv', nrows=20))

    for idx in range(20):
        puzzle = np.reshape(list(sudoku_df.puzzle.values[idx]), (GRID_SIZE, GRID_SIZE)).astype(int)

        start_time = time.time()  # Record start time

        # Main loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(WHITE)
            draw_grid()
            draw_numbers(puzzle)
            pygame.display.update()

            # Solve Sudoku with Maintaining Arc-Consistency and visualize the process
            if solve_sudoku_with_arc_consistency(puzzle):
                pygame.time.delay(3000)  # Pause for a few seconds after solving
                break

        end_time = time.time()  # Record end time
        elapsed_time = end_time - start_time
        print(f"Sudoku {idx + 1} solved with Maintaining Arc-Consistency in {elapsed_time:.2f} seconds.")

    pygame.quit()

if __name__ == "__main__":
    main()
