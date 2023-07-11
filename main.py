import time

import pygame
import random
import queue

# from pprint import PrettyPrinter

pygame.init()

# printer = PrettyPrinter()
WIDTH, HEIGHT = 700, 800

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

BG_COLOR = "white"
ROWS, COLS = 10, 10
MINES = 15
SIZE = WIDTH / ROWS

RECT_COLOR = (200, 200, 200)
CLICKED_RECT_COLOR = (140, 140, 140)
FLAG_RECT_COLOR = "green"
BOMB_RECT_COLOR = "red"
LOST_FONT = pygame.font.SysFont('comicsans', 100)
TIME_FONT = pygame.font.SysFont('comicsans', 50)

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
            if field[r][c] != -1:
                field[r][c] += 1

    return field


def draw(win, field, cover_field, current_time):
    win.fill(BG_COLOR)

    for i, row in enumerate(field):
        y = SIZE * i
        for j, value in enumerate(row):
            x = SIZE * j

            is_covered = cover_field[i][j] == 0
            is_flag = cover_field[i][j] == -2
            is_bomb = value == -1

            if is_flag:
                pygame.draw.rect(win, FLAG_RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(win, "black", (x, y, SIZE, SIZE), 3)
                continue

            if is_covered:
                pygame.draw.rect(win, RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(win, "black", (x, y, SIZE, SIZE), 3)
                continue
            else:
                pygame.draw.rect(win, CLICKED_RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(win, "black", (x, y, SIZE, SIZE), 3)
                if is_bomb:
                    pygame.draw.circle(win, BOMB_RECT_COLOR, (x + SIZE / 2, y + SIZE / 2), SIZE / 3 - 4)

            if value > 0:
                text = NUM_FONT.render(str(value), 1, NUM_COLORS[value])
                win.blit(text, (x + (SIZE / 2 - text.get_width() / 2), y + (SIZE / 2 - text.get_height() / 2)))

    time_text = TIME_FONT.render(f"Time Elapsed: {round(current_time)}", 1, "black")
    win.blit(time_text, (10, (HEIGHT - time_text.get_height())))

    pygame.display.update()


def get_grid_pos(mouse_pos):
    mx, my = mouse_pos
    row = int(my // SIZE)
    col = int(mx // SIZE)
    return row, col


def uncover_from_pos(row, col, cover_field, field):
    q = queue.Queue()
    q.put((row, col))
    visited = set()

    while not q.empty():
        current = q.get()

        neighbours = get_neighbours(*current, ROWS, COLS)
        for r, c in neighbours:
            if (r, c) in visited:
                continue
            value = field[r][c]
            if value == 0 and cover_field[r][c] != -2:
                q.put((r, c))

            if cover_field[r][c] != -2 and field[r][c] != -1:
                cover_field[r][c] = 1

            visited.add((r, c))


def draw_lost(win, text):
    text = LOST_FONT.render(text, 1, "black")
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()


def main():
    run = True
    field = create_mine_field(ROWS, COLS, MINES)
    cover_field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    flags = MINES
    clicks = 0
    lost = False

    start_time = 0
    # printer.pprint(field)
    while run:
        if start_time > 0:
            current_time = time.time() - start_time
        else:
            current_time = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_grid_pos(pygame.mouse.get_pos())
                if row >= ROWS or col >= COLS:
                    continue
                mouse_pressed = pygame.mouse.get_pressed()

                if mouse_pressed[0] and cover_field[row][col] != -2:
                    cover_field[row][col] = 1

                    if field[row][col] == -1:  # If bomb is clicked then reset game
                        lost = True

                    if clicks == 0 or field[row][col] == 0:
                        uncover_from_pos(row, col, cover_field, field)
                    if clicks == 0:
                        start_time = time.time()
                    clicks += 1
                elif mouse_pressed[2]:
                    if cover_field[row][col] == -2:
                        cover_field[row][col] = 0
                        flags += 1
                    else:
                        if flags:
                            if cover_field[row][col] != 1:
                                cover_field[row][col] = -2
                                flags -= 1
        if lost:
            draw(win, field, cover_field, current_time)
            draw_lost(win, "You Lost! Try again..")
            pygame.time.delay(5000)
            # Reset the game
            field = create_mine_field(ROWS, COLS, MINES)
            cover_field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
            flags = MINES
            clicks = 0
            lost = False
            start_time = 0

        draw(win, field, cover_field, current_time)
    pygame.quit()


if __name__ == "__main__":
    main()
