import pygame
from board import *
import time

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 16)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 16)
clock = pygame.time.Clock()

size = (450, 500)
tile_size = 30
cursor = [0, 0]
submit_text = font.render("Submit", False, (255, 255, 255), (50, 50, 50))
submit_button = submit_text.get_rect(center=(400, 475))
get_best_text = font.render("Get Best", False, (255, 255, 255), (50, 50, 50))
get_best_button = get_best_text.get_rect(center=(280, 475))
letters = {}

# Set up the drawing window
screen = pygame.display.set_mode(size)
my_board = Board()


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    get_best()
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        text = self.text
        self.text = ""
        self.txt_surface = FONT.render(self.text, True, self.color)
        return text

    def is_active(self):
        return self.active


input_box = InputBox(20, 465, 40, 20)


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
    input_box.update()
    input_box.draw(screen)


def get_best():
    print("Running...")
    t = time.time_ns()
    best_play, score = my_board.get_best_play(input_box.get_text())
    print(best_play, score)
    print((time.time_ns() - t) / 1000000)
    try:
        my_board.play(best_play)
    except ValueError:
        print("Invalid play")


def handle_key(event):
    if event.key == pygame.K_LEFT:
        cursor[0] = max(0, cursor[0] - 1)
    elif event.key == pygame.K_RIGHT:
        cursor[0] = min(14, cursor[0] + 1)
    elif event.key == pygame.K_UP:
        cursor[1] = max(0, cursor[1] - 1)
    elif event.key == pygame.K_DOWN:
        cursor[1] = min(14, cursor[1] + 1)
    elif event.key == pygame.K_RETURN and not input_box.is_active():
        submit()
    elif 97 <= event.key <= 122 and not input_box.is_active():
        try:
            letters[cursor[1], cursor[0]] = chr(event.key)
        except ValueError:
            pass


def submit():
    global letters
    try:
        print(my_board.score_play(Play(letters)))
        my_board.play(Play(letters))
    except ValueError:
        print("Invalid Play")
    letters = {}


def handle_button_up(event):
    global letters, cursor
    if submit_button.collidepoint(event.pos):
        submit()
    elif get_best_button.collidepoint(event.pos):
        get_best()
    elif event.pos[1] <= 450:
        cursor = [int(i / tile_size) for i in event.pos]


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

            input_box.handle_event(event)

            if event.type == pygame.KEYDOWN:
                handle_key(event)

            if event.type == pygame.MOUSEBUTTONUP:
                handle_button_up(event)

        clock.tick(30)
