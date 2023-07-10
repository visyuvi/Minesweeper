import pygame
import random
from pprint import PrettyPrinter

pygame.init()

printer = PrettyPrinter()
WIDTH, HEIGHT = 700, 800

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

BG_COLOR = "white"
ROWS, COLS = 15, 15
MINES = 15
RECT_COLOR = (200, 200, 200)
CLICKED_RECT_COLOR = (140, 140, 140)

NUM_FONT = pygame.font.SysFont('comicsans', 40)
NUM_COLORS = {1: "black", 2: "indigo", 3: "red", 4: "orange", 5: "yellow", 6: "purple", 7: "blue", 8: "pink", }


def get_neighbours(row, col, rows, cols):
    neighbours = []

    if row > 0:  # UP neighbours
        neighbours.append((row - 1, col))

    if row < rows - 1:  # DOWN neighbours
        neighbours.append((row + 1, col))

    if col > 0:  # LEFT neighbours
        neighbours.append((row, col - 1))

    if col < cols - 1:  # RIGHT neighbours
        neighbours.append((row, col + 1))

    if row > 0 and col > 0:  # TOP LEFT NEIGHBOUR
        neighbours.append((row - 1, col - 1))

    if row < rows - 1 and col < cols - 1:  # BOTTOM RIGHT NEIGHBOUR
        neighbours.append((row + 1, col + 1))

    if row < rows - 1 and col > 0:  # BOTTOM LEFT NEIGHBOUR
        neighbours.append((row + 1, col - 1))

    if row > 0 and col < cols - 1:  # TOP RIGHT NEIGHBOUR
        neighbours.append((row - 1, col + 1))

    return neighbours


def create_mine_field(rows, cols, mines):
    field = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_positions = set()

    while len(mine_positions) < mines:
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)
        pos = row, col

        if pos in mine_positions:
            continue

        mine_positions.add(pos)
        field[row][col] = -1

    for mine in mine_positions:
        neighbours = get_neighbours(*mine, rows, cols)
        for r, c in neighbours:
            field[r][c] += 1

    return field


def draw(win, field, cover_field):
    win.fill(BG_COLOR)

    size = WIDTH / ROWS

    for i, row in enumerate(field):
        y = size * i
        for j, value in enumerate(row):
            x = size * j

            is_covered = cover_field[i][j] == 0
            if is_covered:
                pygame.draw.rect(win, RECT_COLOR, (x, y, size, size))
                pygame.draw.rect(win, "black", (x, y, size, size), 3)
                continue
            else:
                pygame.draw.rect(win, CLICKED_RECT_COLOR, (x, y, size, size))
                pygame.draw.rect(win, "black", (x, y, size, size), 3)

            if value > 0:
                text = NUM_FONT.render(str(value), 1, NUM_COLORS[value])
                win.blit(text, (x + (size/2 - text.get_width()/2), y + (size/2 - text.get_height()/2)))
    pygame.display.update()


def main():
    run = True
    field = create_mine_field(ROWS, COLS, MINES)
    cover_field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    printer.pprint(field)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(win, field, cover_field)
    pygame.quit()


if __name__ == "__main__":
    main()
