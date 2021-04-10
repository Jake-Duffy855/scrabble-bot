import pygame
from board import *
import time

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 16)

size = (450, 500)
tile_size = 30
cursor = [0, 0]
submit_text = font.render("Submit", False, (255, 255, 255), (50, 50, 50))
submit_button = submit_text.get_rect(center=(225, 475))
get_best_text = font.render("Get Best", False, (255, 255, 255), (50, 50, 50))
get_best_button = get_best_text.get_rect(center=(50, 475))
letters = {}

# Set up the drawing window
screen = pygame.display.set_mode(size)
my_board = Board()


def render_board(board: Board):
    for row in range(15):
        for col in range(15):
            if letters.get((row, col), False):
                board_text = letters[row, col].upper()
            else:
                board_text = board.get_text_at(row, col)
            if board_text == 'DW':
                color = (215, 150, 150)
            elif board_text == 'TW':
                color = (225, 20, 0)
            elif board_text == 'DL':
                color = (150, 180, 240)
            elif board_text == 'TL':
                color = (40, 120, 255)
            elif board_text != "":
                color = (200, 160, 130)
            else:
                color = (255, 255, 225)

            # background color
            pygame.draw.rect(screen, color, (tile_size * col, tile_size * row, tile_size, tile_size))

            # text
            text = font.render(board_text, False, (0, 0, 0))
            text_rect = text.get_rect(center=(tile_size * (col + 0.5), tile_size * (row + 0.5)))
            screen.blit(text, text_rect)

            # outline
            pygame.draw.rect(screen, (0, 0, 0), (tile_size * col, tile_size * row, tile_size, tile_size), width=1)

    # cursor
    cur = pygame.Surface((tile_size - 2, tile_size - 2))  # the size of your rect
    cur.set_alpha(150)  # alpha level
    cur.fill((255, 220, 0))  # this fills the entire surface
    screen.blit(cur, (tile_size * cursor[0] + 1, tile_size * cursor[1] + 1))


def render_controls():
    screen.blit(submit_text, submit_button)
    screen.blit(get_best_text, get_best_button)


if __name__ == '__main__':

    # Run until the user asks to quit
    running = True
    while running:

        # Fill the background with white
        screen.fill((255, 255, 255))

        # render board
        render_board(my_board)
        render_controls()

        # Flip the display
        pygame.display.flip()

        # proceed events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # handle MOUSEBUTTONUP

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cursor[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    cursor[0] += 1
                elif event.key == pygame.K_UP:
                    cursor[1] -= 1
                elif event.key == pygame.K_DOWN:
                    cursor[1] += 1
                elif 97 <= event.key <= 122:
                    try:
                        letters[cursor[1], cursor[0]] = chr(event.key)
                    except ValueError:
                        pass

            if event.type == pygame.MOUSEBUTTONUP:
                if submit_button.collidepoint(event.pos):
                    try:
                        print(my_board.score_play(Play(letters)))
                        my_board.play(Play(letters))
                    except ValueError:
                        print("Invalid Play")
                    letters = {}
                elif get_best_button.collidepoint(event.pos):
                    t = time.time_ns()
                    best = my_board.get_best_play(input("Your letters: "))
                    print(best[0], best[1])
                    print((time.time_ns() - t) / 1000000)
                    my_board.play(best[0])
                else:
                    cursor = [int(i / tile_size) for i in event.pos]

            if event.type == pygame.QUIT:
                pygame.quit()
