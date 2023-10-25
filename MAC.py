import pygame #this is the library used to create the interface for the game, It provides modules and functions to handle computer graphics, sound, and user input.
import sys
import numpy as np #NumPy is a Python library for numerical computing, np is an alias name coomonly used by the python comunity.
import pandas as pd # Pandas is a python library that provides data structures, in this project we used DataFrame. 
import time # time is python module that provides time calculating functions

# Constants, these are hardcoded values that will not change throughout the code.
Width, Height = 800, 800 # size of the window that shows the visuals, 
gridSize = 9 #gird size is 9 because domain in 1,2,3,4,5,6,7,8,9
cellSize = Width // gridSize #size of each cell in the suduko visual
#intilizing colors used 
white = (255, 255, 255) 
black = (0, 0, 0)
green = (0, 128, 0)

# initialize pygame
pygame.init() #starting the visual interface to see the game

# display screen
screen = pygame.display.set_mode((Width, Height)) # using pygame.display for display
pygame.display.set_caption("Sudoku solving visualizer for CS361, MaintainingArcConsistency.") 

# initialize the font and size
font = pygame.font.Font(None, 36)

def makeGrid(): #here we define the function that makes the grid outline that will be displays on screen
    
    for i in range(1, gridSize): #iterate from 1 to gridSize - 1
        if i % 3 == 0: 
            # If i is divisible by 3,  draw a vertical line on the screen
            pygame.draw.line(screen, black, (i * cellSize, 0), (i * cellSize, Height), 3)
            pygame.draw.line(screen, black, (0, i * cellSize), (Width, i * cellSize), 3)
        else:
            # if i is divisible by 3, draw a horizontal line
            pygame.draw.line(screen, black, (i * cellSize, 0), (i * cellSize, Height))
            pygame.draw.line(screen, black, (0, i * cellSize), (Width, i * cellSize))

def makeNumbers(grid):
    # Draw numbers on the grid
    for i in range(gridSize): #outer loop that iterates over the rows of the grid
        for j in range(gridSize): # inner loop that iterates over the columns of the grid
            if grid[i][j] != 0: #checks if the value in the current cell of the grid is not equal to 0
                num = font.render(str(grid[i][j]), True, black) #convert value from the grid into a string using str() then turn it into text iamge using pygame font and store it in num
                screen.blit(num, (j * cellSize + 20, i * cellSize + 20)) #draws text image num onto the Pygame screen.

def clearCell(row, col):
    pygame.draw.rect(screen, white, (col * cellSize, row * cellSize, cellSize, cellSize)) #draw a white rectangle over the screen to clear or erase the screen
    makeGrid()  # then draw grid lines again

def isSafeSlot(puzzle, row, col, num):
    # Check if the number is not already present in the row, column, and the current 3x3 square
    return (
        all(num != puzzle[row][i] for i in range(gridSize)) and #checks if num is not present in the specified row
        all(num != puzzle[i][col] for i in range(gridSize)) and #checks if num is not present in the specified column
        all(num != puzzle[row - row % 3 + i][col - col % 3 + j] for i in range(3) for j in range(3)) # check if num is present in a 3x3 square by using the modulo operator to find the left top (first) cell then iterating over each cell to compare it to the square numbers
    )


def applyAC(puzzle, row, col, num): #apply arc consistency method
    
    for i in range(gridSize):#iterate over the row
        if i != col: #if the current cell is not the same as the cell we are checking ...
            puzzle[row][i] = np.delete(puzzle[row][i], np.where(puzzle[row][i] == num)) # then delete the num from the domain of the cell

    
    for i in range(gridSize):#iterate over the column
        if i != row:
            puzzle[i][col] = np.delete(puzzle[i][col], np.where(puzzle[i][col] == num)) 

    # Apply arc consistency in the square
    square_row, square_col = 3 * (row // 3), 3 * (col // 3) #find the top left cell of the square
    for i in range(square_row, square_row + 3): #iterate over the rows of the square
        for j in range(square_col, square_col + 3): #iterate over the columns of the square
            if i != row or j != col: #if the current cell is not the same as the cell we are checking ...
                puzzle[i][j] = np.delete(puzzle[i][j], np.where(puzzle[i][j] == num)) # then delete the num from the domain of the cell

def solutionMAC(puzzle): #solution using maintiaintm arc consistency method
    for event in pygame.event.get(): #get the events from the pygame
        if event.type == pygame.QUIT: #pygame.QUIT is the event type that is fired when the user clicks on the close button of the window
            pygame.quit() #pygame.quit() is used to uninitialize all pygame modules
            sys.exit() #sys.exit() is used to exit the program

    for i in range(gridSize): #outer loop that iterates over the rows of the grid
        for j in range(gridSize): # inner loop that iterates over the columns of the grid
            if puzzle[i][j] == 0: #checks if the value in the current cell of the grid is equal to 0
                for num in range(1, 10): #iterate from 1 to 9
                    if isSafeSlot(puzzle, i, j, num): #checks if the current cell is safe to place the number in using the predefined function isSafeSlot()
                        pygame.time.delay(100) #delay the program for 100 milliseconds for visualization purposes, so that the visual isnt too fast
                        makeNumbers(puzzle) #draw the numbers on the screen
                        pygame.display.update() #update the current screen display

                        clearCell(i, j)  # Clear the cell
                        pygame.display.update() #update the current screen display

                        puzzle[i][j] = num #assign the current cell to the number
                        applyAC(puzzle, i, j, num) #apply arc consistency
                        makeNumbers(puzzle) #
                        pygame.display.update()

                        if solutionMAC(puzzle): #recursively call the function solutionBT() to solve the rest of the puzzle
                            return True

                        pygame.time.delay(100) 
                        puzzle[i][j] = 0 #if the puzzle is not solved, assign the current cell to 0
                        makeNumbers(puzzle) 
                        pygame.display.update()

                return False

    return True

def main():
    # Read Sudoku data
    sudoku_df = pd.DataFrame(pd.read_csv('sudoku.csv', nrows=20)) #read the first 20 rows of the csv file and store it in a dataframe

    for idx in range(20): #iterate from 0 to 19
        puzzle = np.reshape(list(sudoku_df.puzzle.values[idx]), (gridSize, gridSize)).astype(int) #reshape the puzzle(the 20 nums taken) into a 9x9 grid

        StartingTime = time.time()  # Record start time

        # Main loop
        while True:
            for event in pygame.event.get(): #
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(white) #fill the screen with white color to erase the screen / clear the screen
            makeGrid() #draw new grid lines
            makeNumbers(puzzle) 
            pygame.display.update()

            # Solve Sudoku with Maintaining Arc-Consistency and visualize the process
            if solutionMAC(puzzle): 
                pygame.time.delay(5000)  # Pause for a 5 seconds after solving so the user gets a chance to see the solution before it starts displaying the next puzzle
                break #break out of the loop

        endTime = time.time()  # Record end time
        elapsedTime = endTime - StartingTime
        print(f"Sudoku {idx + 1} solved with Maintaining Arc-Consistency in {elapsedTime:.2f} seconds.") #print the elapsed time using f string

    pygame.quit()

if __name__ == "__main__":
    main()
