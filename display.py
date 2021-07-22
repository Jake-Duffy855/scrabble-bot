import pygame
from board import *
import time

pygame.init()
pygame.font.init()
pygame.display.set_caption("Scrabble")
font = pygame.font.SysFont("Arial", 16)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 16)
clock = pygame.time.Clock()

size = (450, 550)
tile_size = 30
cursor = [7, 7]
submit_text = font.render("Submit", False, (255, 255, 255), (50, 50, 50))
submit_button = submit_text.get_rect(center=(420, 475))
get_best_text = font.render("Get Best", False, (255, 255, 255), (50, 50, 50))
get_best_button = get_best_text.get_rect(center=(260, 475))
remove_last_text = font.render("Remove Last", False, (255, 255, 255), (50, 50, 50))
remove_last_button = remove_last_text.get_rect(center=(342, 475))
get_recap_text = font.render("Recap", False, (255, 255, 255), (50, 50, 50))
get_recap_button = get_recap_text.get_rect(center=(40, 525))
next_turn_text = font.render("Next Turn", False, (255, 255, 255), (50, 50, 50))
next_turn_button = next_turn_text.get_rect(center=(115, 525))
prev_turn_text = font.render("Prev Turn", False, (255, 255, 255), (50, 50, 50))
prev_turn_button = prev_turn_text.get_rect(center=(200, 525))
show_best_text = font.render("Show Best", False, (255, 255, 255), (50, 50, 50))
show_best_button = show_best_text.get_rect(center=(290, 525))
show_actual_text = font.render("Show Actual", False, (255, 255, 255), (50, 50, 50))
show_actual_button = show_actual_text.get_rect(center=(390, 525))
letters = {}
plays = []
best_plays = []
tiles_had = []
recap = False
turn = 0

# Set up the drawing window
screen = pygame.display.set_mode(size)
my_board = Board()


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_ACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = True

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
    add_highlight(cursor[0], cursor[1])

    # highlight last play
    if len(plays) > 0:
        for row, col in plays[-1].letters:
            add_highlight(col, row, color=(100, 250, 100))


def add_highlight(x, y, color=(255, 220, 0)):
    cur = pygame.Surface((tile_size - 2, tile_size - 2))  # the size of your rect
    cur.set_alpha(150)  # alpha level
    cur.fill(color)  # this fills the entire surface
    screen.blit(cur, (tile_size * x + 1, tile_size * y + 1))


def render_controls():
    screen.blit(submit_text, submit_button)
    screen.blit(get_best_text, get_best_button)
    screen.blit(remove_last_text, remove_last_button)
    screen.blit(get_recap_text, get_recap_button)
    screen.blit(next_turn_text, next_turn_button)
    screen.blit(prev_turn_text, prev_turn_button)
    screen.blit(show_actual_text, show_actual_button)
    screen.blit(show_best_text, show_best_button)
    input_box.update()
    input_box.draw(screen)


def get_best():
    print("Running...")
    t = time.time_ns()
    text = input_box.get_text()
    if len(text) <= 7:
        best_play, score = my_board.get_best_play(text)
        tiles_had.append(text)
        best_plays.append(best_play)
        # print(best_play, score)
        print((time.time_ns() - t) / 1000000)
        # try:
        #     my_board.play(best_play)
        #     plays.append(best_play.letters.copy())
        # except ValueError:
        #     print("Invalid play")

    else:
        print("Please enter up to 7 letters.")


def remove_last():
    """
    Remove the play stored in last play from the board
    :return: None
    """
    try:
        my_board.remove_play(plays[-1])
        plays.pop()
    except ValueError:
        print("No play to remove.")


def handle_key(event):
    if not input_box.is_active():
        if event.key == pygame.K_LEFT:
            cursor[0] = max(0, cursor[0] - 1)
        elif event.key == pygame.K_RIGHT:
            cursor[0] = min(14, cursor[0] + 1)
        elif event.key == pygame.K_UP:
            cursor[1] = max(0, cursor[1] - 1)
        elif event.key == pygame.K_DOWN:
            cursor[1] = min(14, cursor[1] + 1)
        elif event.key == pygame.K_RETURN:
            submit()
        elif event.key == pygame.K_DELETE or event.key == 8:
            handle_delete()
        elif 97 <= event.key <= 122:
            try:
                letters[cursor[1], cursor[0]] = chr(event.key)
            except ValueError:
                pass


def submit():
    global letters, last_play
    try:
        print(my_board.score_play(Play(letters)))
        my_board.play(Play(letters))
        plays.append(Play(letters.copy()))
    except ValueError:
        print("Invalid Play")
    letters = {}


def handle_button_up(event):
    global letters, cursor
    if submit_button.collidepoint(event.pos):
        submit()
    elif get_best_button.collidepoint(event.pos):
        get_best()
    elif remove_last_button.collidepoint(event.pos):
        remove_last()
    elif get_recap_button.collidepoint(event.pos):
        get_game_recap()
    elif next_turn_button.collidepoint(event.pos):
        get_next_turn()
    elif prev_turn_button.collidepoint(event.pos):
        get_previous_turn()
    elif show_best_button.collidepoint(event.pos):
        show_best()
    elif show_actual_button.collidepoint(event.pos):
        show_actual()
    elif event.pos[1] <= 450:
        cursor = [int(i / tile_size) for i in event.pos]


def handle_delete():
    row, col = cursor[1], cursor[0]
    if letters.get((row, col), False):
        letters.pop((row, col))


def get_next_turn():
    global turn, best_play, actual_play
    show_actual()
    turn += 1
    actual_play = plays[turn]
    best_play = best_plays[turn]
    print(tiles_had[turn])
    print(actual_play, my_board.score_play(actual_play))
    print(best_play, my_board.score_play(best_play))


def get_previous_turn():
    global turn, best_play, actual_play
    show_actual()
    if turn > 0:
        turn -= 1
        my_board.remove_play(best_play)
        my_board.remove_play(actual_play)
        actual_play = plays[turn]
        best_play = best_plays[turn]
        print(tiles_had[turn])
        print(actual_play, my_board.score_play(actual_play))
        print(best_play, my_board.score_play(best_play))


def get_game_recap():
    global my_board, turn, best_play, actual_play
    my_board = Board()
    actual_play = plays[turn]
    best_play = best_plays[turn]
    plays.append(actual_play)
    print(tiles_had[turn])
    print(actual_play, my_board.score_play(actual_play))
    print(best_play, my_board.score_play(best_play))


def show_actual():
    global turn, best_play, actual_play
    my_board.remove_play(best_play)
    my_board.remove_play(actual_play)
    my_board.play(actual_play)
    plays[-1] = actual_play


def show_best():
    global turn, best_play, actual_play
    my_board.remove_play(best_play)
    my_board.remove_play(actual_play)
    my_board.play(best_play)
    plays[-1] = best_play


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
