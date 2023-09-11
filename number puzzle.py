
import pygame
import random
import pyautogui
from pygame.locals import *

pygame.mixer.init()
click_sound = pygame.mixer.Sound('sound effect.mp3')

# Define a class for individual puzzle tiles
class Tile:
    def __init__(self, screen, start_x, start_y, number, row, col):
        self.color = (0, 255, 0)
        self.screen = screen
        self.x = start_x
        self.y = start_y
        self.number = number
        self.width = tile_width
        self.height = tile_height
        self.selected = False
        self.row = row
        self.col = col
        self.movable = False

    def draw(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
        number_text = font.render(str(self.number), True, (0, 0, 0))
        screen.blit(number_text, (self.x + 40, self.y + 10))

    def hover(self, mouse_x, mouse_y):
        if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
            self.color = (255, 255, 255)
        else:
            self.color = (205, 127, 50)

    def click(self, mouse_x, mouse_y):
        if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
            self.selected = True
        else:
            self.selected = False

    def release_click(self, release_x, release_y):
        if release_x > 0 and release_y > 0:
            self.selected = False

    def move(self, mouse_x, mouse_y):
        self.x = mouse_x
        self.y = mouse_y

    def click(self, mouse_x, mouse_y):
        if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
            self.selected = True
            click_sound.play()  # Play the audio clip
        else:
            self.selected = False

    def release_click(self, release_x, release_y):
        if release_x > 0 and release_y > 0:
            self.selected = False
            click_sound.stop()  # Stop the audio clip when releasing the click

# Function to create the puzzle tiles
def create_tiles():
    tile_numbers = list(range(1, tile_count + 1))
    random.shuffle(tile_numbers)
    tile_numbers.append("")  # Add an empty space
    k = 0
    for i in range(rows):
        for j in range(cols):
            if i == rows - 1 and j == cols - 1:
                continue  # Skip the last empty space
            else:
                t = Tile(screen, tile_positions[(i, j)][0], tile_positions[(i, j)][1], tile_numbers[k], i, j)
                puzzle_tiles.append(t)
            puzzle_matrix[i][j] = tile_numbers[k]
            k += 1
    check_tile_movability()

# Function to check if a tile can be moved to a certain position
def check_tile_movability():
    for i in range(tile_count):
        tile = puzzle_tiles[i]
        tile_row = tile.row
        tile_col = tile.col
        adjacent_cells = []
        adjacent_cells.append([tile_row - 1, tile_col, False])  # Up
        adjacent_cells.append([tile_row + 1, tile_col, False])  # Down
        adjacent_cells.append([tile_row, tile_col - 1, False])  # Left
        adjacent_cells.append([tile_row, tile_col + 1, False])  # Right

        for j in range(len(adjacent_cells)):
            if 0 <= adjacent_cells[j][0] < rows and 0 <= adjacent_cells[j][1] < cols:
                adjacent_cells[j][2] = True

        for k in range(len(adjacent_cells)):
            if adjacent_cells[k][2]:
                adj_cell_row = adjacent_cells[k][0]
                adj_cell_col = adjacent_cells[k][1]
                for m in range(tile_count):
                    if adj_cell_row == puzzle_tiles[m].row and adj_cell_col == puzzle_tiles[m].col:
                        adjacent_cells[k][2] = False

                false_count = 0

                for n in range(len(adjacent_cells)):
                    if adjacent_cells[n][2]:
                        tile.movable = True
                        break
                    else:
                        false_count += 1

                if false_count == 4:
                    tile.movable = False

# Check if the puzzle is solved
def is_puzzle_solved():
    global game_over, game_over_message
    all_tile_data = ""
    for i in range(rows):
        for j in range(cols):
            all_tile_data = all_tile_data + str(puzzle_matrix[i][j])

    if all_tile_data == "12345678 ":
        game_over = True
        game_over_message = "Game Over. Congratulations!"

        print("Game Over. Congratulations!")

        for i in range(tile_count):
            puzzle_tiles[i].movable = False
            puzzle_tiles[i].selected = False

# Set up window dimensions
window_width, window_height = pyautogui.size()
window_width = int(window_width * 0.95)
window_height = int(window_height * 0.95)

# Set tile dimensions
puzzle_tiles = []
tile_width = 200
tile_height = 200

# Set number of rows and columns for the puzzle
rows, cols = (3, 3)
tile_count = rows * cols - 1
puzzle_matrix = [["" for i in range(cols)] for j in range(rows)]
tile_numbers = []
tile_positions = {
    (0, 0): (100, 50),
    (0, 1): (305, 50),
    (0, 2): (510, 50),
    (1, 0): (100, 255),
    (1, 1): (305, 255),
    (1, 2): (510, 255),
    (2, 0): (100, 460),
    (2, 1): (305, 460),
    (2, 2): (510, 460),
}

# Initialize variables
mouse_pressed = False
mouse_x_click, mouse_y_click = 0, 0
mouse_x_release, mouse_y_release = 0, 0
game_over = False
game_over_message = ""

# Initialize pygame and set the caption
pygame.init()
game_over_font = pygame.font.Font('freesansbold.ttf', 70)
move_count = 0
move_count_message = "Moves: "
move_count_font = pygame.font.Font('freesansbold.ttf', 40)
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Slide Puzzle")
font = pygame.font.Font('freesansbold.ttf', 200)

# Create the puzzle tiles
create_tiles()

running = True
while running:
    screen.fill((110, 38, 14))  # Fill the screen with black

    # Draw the puzzle board
    pygame.draw.rect(screen, (165, 42, 42), pygame.Rect(95, 45, 620, 620))
    game_over_print = game_over_font.render(game_over_message, True, (255, 255, 0))

    screen.blit(game_over_print, (950, 100))

    # Render the move_count
    if move_count == 0:
        move_count_render = move_count_font.render(move_count_message, True, (255, 215, 0))
    else:
        move_count_render = move_count_font.render(move_count_message + str(move_count), True, (255, 215, 0))
    screen.blit(move_count_render, (1050, 200))

    # Get events from the queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i in range(tile_count):
                puzzle_tiles[i].hover(mouse_x, mouse_y)

            for i in range(tile_count):
                if puzzle_tiles[i].selected and mouse_pressed:
                    puzzle_tiles[i].move(mouse_x, mouse_y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
            mouse_x_click, mouse_y_click = pygame.mouse.get_pos()
            for i in range(tile_count):
                puzzle_tiles[i].click(mouse_x_click, mouse_y_click)

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
            mouse_x_release, mouse_y_release = pygame.mouse.get_pos()
            mouse_x_click, mouse_y_click = 0, 0
            cell_found = False
            for i in range(rows):
                for j in range(cols):
                    tile_start_x = tile_positions[(i, j)][0]
                    tile_start_y = tile_positions[(i, j)][1]

                    if (mouse_x_release > tile_start_x and mouse_x_release < tile_start_x + tile_width) and (mouse_y_release > tile_start_y and mouse_y_release < tile_start_y + tile_height):
                        if puzzle_matrix[i][j] == "":
                            for k in range(tile_count):
                                if game_over == False:
                                    if puzzle_tiles[k].selected:
                                        if puzzle_tiles[k].movable:
                                            cell_found = True
                                            dummy = puzzle_matrix[puzzle_tiles[k].row][puzzle_tiles[k].col]
                                            puzzle_matrix[puzzle_tiles[k].row][puzzle_tiles[k].col] = puzzle_matrix[i][j]
                                            puzzle_matrix[i][j] = dummy
                                            puzzle_tiles[k].row = i
                                            puzzle_tiles[k].col = j
                                            puzzle_tiles[k].x = tile_positions[(i, j)][0]
                                            puzzle_tiles[k].y = tile_positions[(i, j)][1]
                                            move_count += 1
                                            is_puzzle_solved()
                                            check_tile_movability()

                    if not cell_found:
                        for k in range(tile_count):
                            if puzzle_tiles[k].selected:
                                row_pos = puzzle_tiles[k].row
                                col_pos = puzzle_tiles[k].col
                                puzzle_tiles[k].x = tile_positions[(row_pos, col_pos)][0]
                                puzzle_tiles[k].y = tile_positions[(row_pos, col_pos)][1]
                                break

    for i in range(tile_count):
        puzzle_tiles[i].draw()

    pygame.display.flip()

pygame.display.update()