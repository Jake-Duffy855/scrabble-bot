from scrabble import is_valid, all_length_perms, values
from squares import *
from play import *
from word import *
import time


class Board:
    """Model to represent the board in scrabble"""

    def __init__(self):
        self.init_squares()
        self.letters = [["" for i in range(15)] for j in range(15)]

    def init_squares(self):
        self.squares = [[Square() for i in range(15)] for j in range(15)]

        # add double words
        for loc in double_words:
            self.squares[loc[0]][loc[1]] = DoubleWord()
        # add triple words
        for loc in triples_words:
            self.squares[loc[0]][loc[1]] = TripleWord()
        # add double letters
        for loc in double_letters:
            self.squares[loc[0]][loc[1]] = DoubleLetter()
        # add triple letters
        for loc in triple_letters:
            self.squares[loc[0]][loc[1]] = TripleLetter()

    def score_play(self, play: Play) -> int:
        """
        Score the given play
        :param play: the play to score
        :return: the score of the given play
        """
        score = 0
        if self.is_valid_play(play):
            for word in self.get_all_words_from_play(play):
                word_score = 0
                word_multiplier = 1
                for loc in word.letters:
                    word_score += values[word.letters[loc]] * \
                                  self.get_letter_multiplier(loc, word.played.get(loc, False))
                    word_multiplier *= self.get_word_multiplier(loc, word.played.get(loc, False))
                score += word_score * word_multiplier
            if len(play.letters) == 7:
                score += 50
        return score

    def get_best_play(self, letters: list) -> Play:
        """
        Returns the highest score play possible with the given letters
        :param letters: The list of letters that are able to be played
        :return: The play with the highest score using the given letters
        """
        word = "".join(letters)
        perms = all_length_perms(word)
        best_play = Play({(7, 7): "a"})
        best_score = 0
        if self.letters == [["" for i in range(15)] for j in range(15)]:
            perms = list(filter(lambda x: is_valid(x), perms))
            for col in range(1, 8):
                for w in perms:
                    play = self.generate_play_starting_at(w, 7, col, True)
                    score = self.score_play(play)
                    if score > best_score or (score == best_score and len(play.letters) > len(best_play.letters)):
                        best_score, best_play = score, play

        else:
            for row in range(15):
                for col in range(15):
                    # if self.letters[row][col] != "" and self.next_to_letter(row, col):
                    print(row, col)
                    for w in perms:
                        bools = [True, False]
                        if row + len(w) > 15:
                            bools.remove(False)
                        elif col + len(w) > 15:
                            bools.remove(True)
                        for b in bools:
                            play = self.generate_play_starting_at(w, row, col, b)
                            score = self.score_play(play)
                            if score > best_score or \
                                    (score == best_score and len(play.letters) > len(best_play.letters)):
                                best_score, best_play = score, play

        return best_play, best_score

    def generate_play_starting_at(self, word: str, row: int, col: int, right: bool):
        if right:
            dx, dy = 0, 1
        else:
            dx, dy = 1, 0

        play = {}
        for letter in word:
            while row < 15 and col < 15 and self.letters[row][col] != "":
                row += dx
                col += dy
            if row < 15 and col < 15:
                play[row, col] = letter
                row += dx
                col += dy
            else:
                return Play({(7, 7): "a"})
        return Play(play)

    def play(self, play: Play):
        if self.is_valid_play(play):
            for loc in play.letters:
                self.letters[loc[0]][loc[1]] = play.letters[loc]
        else:
            raise ValueError("This play is invalid")

    def get_all_words_from_play(self, play: Play) -> list:
        """
        Returns all the words made by the given play
        :param play: The play to be made
        :return: A list of words that are created from the given play
        """
        result = []
        first_loc = list(play.letters.keys())[0]

        if play.same_xs():
            func = self.get_vertical_word
            main_word = self.get_horizontal_word(play.letters[first_loc], first_loc, play.letters)
        else:
            func = self.get_horizontal_word
            main_word = self.get_vertical_word(play.letters[first_loc], first_loc, play.letters)

        if len(main_word.word) > 1:
            result.append(main_word)

        for loc in sorted(play.letters.keys()):
            word = func(play.letters[loc], loc, play.letters)
            if len(word.word) > 1:
                result.append(word)
        return result

    def is_connected(self, play: Play) -> bool:
        """
        Does the given Play connect to present words or is it the first word
        :param play: the play to determine
        :return: True if connected, False is not
        """
        if self.letters == [["" for i in range(15)] for j in range(15)] and (7, 7) in play.letters.keys():

            return True

        for loc in play.letters:
            try:
                if 14 >= loc[0] + 1 and self.letters[loc[0] + 1][loc[1]] != "":
                    return True
                elif 0 <= loc[0] - 1 and self.letters[loc[0] - 1][loc[1]] != "":
                    return True
                elif 14 >= loc[1] + 1 and self.letters[loc[0]][loc[1] + 1] != "":
                    return True
                elif 0 <= loc[1] - 1 and self.letters[loc[0]][loc[1] - 1] != "":
                    return True
            except IndexError:
                pass
        return False

    def is_consecutive(self, play: Play) -> bool:
        """
        Is the given play in a row, without gaps
        :param play: the play to verify
        :return: True if the play is consecutive, False if not
        """
        if play.same_xs():
            ys = set()
            x = list(play.letters.keys())[0][0]
            for loc in play.letters:
                ys.add(loc[1])
            low = min(ys)
            high = max(ys)
            consec = set(range(low, high + 1))
            gaps = consec - ys
            for y in gaps:
                if self.letters[x][y] == "":
                    return False
        else:
            xs = set()
            y = list(play.letters.keys())[0][1]
            for loc in play.letters:
                xs.add(loc[0])
            low = min(xs)
            high = max(xs)
            consec = set(range(low, high + 1))
            gaps = consec - xs
            for x in gaps:
                if self.letters[x][y] == "":
                    return False
        return True

    def has_letter_at(self, row, col) -> bool:
        return (0 <= row <= 14) and (0 <= col <= 14) and self.letters[row][col] != ""

    def next_to_letter(self, row, col) -> bool:
        return self.has_letter_at(row - 1, col) \
               or self.has_letter_at(row + 1, col) \
               or self.has_letter_at(row, col - 1) \
               or self.has_letter_at(row, col + 1)

    def is_legal(self, play: Play) -> bool:
        """
        Verifies that the given play has no overlaps
        :param play: The play to be verified
        :return: True if the play is legal, False otherwise
        """
        for loc in play.letters:
            if self.letters[loc[0]][loc[1]] != "":
                return False
        return True

    def is_valid_play(self, play: Play) -> bool:
        """
        Is the given play a valid play
        :param play: The given play
        :return: True if the play is valid, False if not
        """
        for word in self.get_all_words_from_play(play):
            if not is_valid(word.word):
                return False
        return self.is_legal(play) and self.is_connected(play) and self.is_consecutive(play)

    def get_vertical_word(self, letter: str, loc: tuple, letters: dict) -> Word:
        word = {loc: letter}
        played = dict.fromkeys(letters.keys(), True)
        x = loc[0]
        y = loc[1]
        while x > 0 and (self.letters[x - 1][y] or (x - 1, y) in letters):
            if self.letters[x - 1][y]:
                word[x - 1, y] = self.letters[x - 1][y]
            else:
                word[x - 1, y] = letters[x - 1, y]
            x -= 1
        x = loc[0]
        while x < 14 and (self.letters[x + 1][y] or (x + 1, y) in letters):
            if self.letters[x + 1][y]:
                word[x + 1, y] = self.letters[x + 1][y]
            else:
                word[x + 1, y] = letters[x + 1, y]
            x += 1
        return Word(word, played)

    def get_horizontal_word(self, letter: str, loc: tuple, letters: dict) -> Word:
        word = {loc: letter}
        played = dict.fromkeys(letters.keys(), True)
        x = loc[0]
        y = loc[1]
        while y > 0 and (self.letters[x][y - 1] or (x, y - 1) in letters):
            if self.letters[x][y - 1]:
                word[x, y - 1] = self.letters[x][y - 1]
            else:
                word[x, y - 1] = letters[x, y - 1]
            y -= 1
        y = loc[1]
        while y < 14 and (self.letters[x][y + 1] or (x, y + 1) in letters):
            if self.letters[x][y + 1]:
                word[x, y + 1] = self.letters[x][y + 1]
            else:
                word[x, y + 1] = letters[x, y + 1]
            y += 1
        return Word(word, played)

    def get_letter_multiplier(self, loc: tuple, played: bool):
        if played:
            return self.squares[loc[0]][loc[1]].get_letter_multiplier()
        return 1

    def get_word_multiplier(self, loc: tuple, played: bool):
        if played:
            return self.squares[loc[0]][loc[1]].get_word_multiplier()
        return 1

    def __str__(self):
        result = ""
        for row in range(15):
            for col in range(15):
                if self.letters[row][col]:
                    result += self.letters[row][col].upper() + " "
                else:
                    result += str(self.squares[row][col])
            result += "\n"
        return result


# -------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    my_board = Board()
    my_board.play(Play({
        (7, 7): "e",
        (7, 6): "t",
        (7, 5): "l",
        (7, 4): "o",
        (7, 3): "v",
    }))
    my_board.play(Play({
        (3, 3): "s",
        (4, 3): "a",
        (5, 3): "l",
        (6, 3): "i",
        (8, 3): "a",
    }))
    my_board.play(Play({
        (8, 2): "b",
        (9, 2): "o",
        (10, 2): "t",
        (11, 2): "t",
        (12, 2): "e"}))
    my_board.play(Play({
        (0, 7): "m",
        (1, 7): "i",
        (2, 7): "s",
        (3, 7): "q",
        (4, 7): "u",
        (5, 7): "o",
        (6, 7): "t"}))
    my_board.play(Play({
        (1, 8): "s",
        (2, 8): "h",
        (3, 8): "i",
        (4, 8): "r",
        (5, 8): "e"}))
    my_board.play(Play({
        (9, 1): "w",
        (10, 1): "e",
        (11, 1): "a",
        (12, 1): "r",
        (13, 1): "s"}))
    my_board.play(Play({
        (11, 0): "v",
        (12, 0): "o",
        (13, 0): "i",
        (14, 0): "d"}))
    my_board.play(Play({
        (2, 4): "f",
        (3, 4): "o",
        (4, 4): "x"}))
    my_board.play(Play({
        (1, 5): "j",
        (2, 5): "a",
        (3, 5): "n",
        (4, 5): "e"}))
    my_board.play(Play({
        (8, 5): "a",
        (8, 6): "e",
        (8, 7): "r",
        (8, 8): "y"}))
    my_board.play(Play({
        (9, 4): "o",
        (9, 5): "p"}))
    my_board.play(Play({
        (9, 8): "a",
        (9, 9): "r",
        (9, 10): "r",
        (9, 11): "a",
        (9, 12): "i",
        (9, 13): "g",
        (9, 14): "n"}))
    my_board.play(Play({
        (6, 4): "n",
        (6, 5): "c",
        (6, 6): "u"}))
    my_board.play(Play({
        (7, 14): "g",
        (8, 14): "e",
        (10, 14): "t",
        (11, 14): "y"}))
    my_board.play(Play({
        (11, 8): "u",
        (11, 9): "n",
        (11, 10): "d",
        (11, 11): "e",
        (11, 12): "i",
        (11, 13): "f"}))
    my_board.play(Play({
        (2, 9): "o",
        (3, 9): "n",
        (4, 9): "e"}))
    my_board.play(Play({
        (0, 9): "r",
        (1, 9): "h"}))
    print(my_board)

    t = time.time_ns()
    best = my_board.get_best_play("wgelksu".split())
    print(best[0], best[1])
    print((time.time_ns() - t) / 1000000)
    my_board.play(best[0])
    print(my_board)

    # while True:
    #     letters = input("Letters: ")
    #     t = time.time_ns()
    #     best = my_board.get_best_play(letters.split())
    #     print(best[0], best[1])
    #     print((time.time_ns() - t) / 1000000)
    #     my_board.play(best[0])
    #     print(my_board)
