from scrabble import is_valid, all_length_perms, values, is_valid_perm, generate_blank_replacements
from squares import *
from play import *
from word import *
import time


class Board:
    """Model to represent the board in scrabble"""

    def __init__(self):
        self.squares = []
        self.init_squares()
        self.letters = [["" for i in range(15)] for j in range(15)]
        # (length, right_bool): [locs]
        self.playable_areas = {}
        self.init_playable_areas()

    def init_squares(self):
        """
        Generate the board with all the bonus squares
        """
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

    def init_playable_areas(self):
        """
        Initialize the playable areas for all length plays
        """
        self.playable_areas = {(length, b): set() for length in range(1, 8) for b in [True, False]}
        for length in range(1, 8):
            for col in range(length):
                self.playable_areas[length, True].add((7, 7 - col))

    def update_playable_areas(self, play: Play, first_play: bool):
        """
        Update the playable areas for each length play based on the given play
        :param play: the play that will affect the playable areas
        :param first_play: is this play the first play
        """
        if first_play:
            self.playable_areas = {(length, b): set() for length in range(1, 8) for b in [True, False]}
        # remove the spaces in that play from all playable areas
        for loc in play.letters:
            for playable_area in self.playable_areas:
                try:
                    self.playable_areas[playable_area].remove(loc)
                except KeyError:
                    pass
        # add all new playable spaces
        for loc in play.letters:
            self.add_playable_area_from_loc(loc)

    def add_playable_area_from_loc(self, loc: tuple, recur=True):
        """
        Add all reachable locations from the given loc to the playable areas
        :param loc: the location from which to extend the playable areas
        :param recur: whether to add reachable squares from surrounding tiles as well
        """
        row, col = loc

        if recur:
            diff = 0
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row, new_col = row + dx, col + dy
                self.add_playable_area_from_loc((new_row, new_col), False)
        else:
            diff = 1

        if 0 <= row <= 14 and 0 <= col <= 14 and self.letters[row][col] == "":
            for playable_area in [(length, b) for length in range(1, 8) for b in [True, False]]:
                self.playable_areas[playable_area].add((row, col))

        for dist in range(1, 8 - diff):
            for right_going in [True, False]:
                dx, dy = {True: (0, -dist), False: (-dist, 0)}[right_going]
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row <= 14 and 0 <= new_col <= 14 and self.letters[new_row][new_col] == "":
                    for length in range(dist + diff, 8):
                        self.playable_areas[length, right_going].add((new_row, new_col))

    def score_play(self, play: Play) -> int:
        """
        Score the given play
        :param play: the play to score
        :return: the score of the given play
        """
        score = 0
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
        # if "s" in play.letters.values() or "q" in play.letters.values() or "z" in play.letters.values():
        #     score -= 5
        return score

    def get_best_play(self, letters: str) -> tuple:
        """
        Returns the highest score play possible with the given letters
        :param letters: The list of letters that are able to be played
        :return: The play with the highest score using the given letters
        """
        start_time = time.time()
        best_play = Play({(7, 7): "a"})
        best_score = 0
        if self.letters == [["" for i in range(15)] for j in range(15)]:
            perms = all_length_perms(letters, first=True)
            if "?" in letters:
                for perm in perms:
                    if "?" not in perm and not is_valid(perm):
                        perms.remove(perm)
            else:
                perms = list(filter(lambda x: is_valid(x), perms))
        else:
            perms = all_length_perms(letters)
        perms = sorted(perms, key=lambda x: len(x), reverse=True)
        for w in perms:
            if time.time() - start_time >= 180:
                print(w)
                return best_play, best_score
            bools = [True, False]
            for right_going in bools:
                for loc in self.playable_areas[len(w), right_going]:
                    row, col = loc
                    play = self.generate_play_starting_at(w, row, col, right_going)
                    if "?" in w:
                        score = self.score_play(play)
                        if score > best_score:
                            valid, play = self.is_valid_play_with_blank(play)
                            if valid:
                                best_score, best_play = score, play
                    else:
                        if self.is_valid_play(play):
                            score = self.score_play(play)
                            if score > best_score:
                                best_score, best_play = score, play
        return best_play, best_score

    def generate_play_starting_at(self, word: str, row: int, col: int, right: bool) -> Play:
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
        if self.letters == [["" for i in range(15)] for j in range(15)]:
            first_play = True
        else:
            first_play = False
        if "?" in play.letters.values():
            result = self.is_valid_play_with_blank(play)
            if result[0]:
                valid = True
                play = result[1]
            else:
                valid = False
        else:
            valid = self.is_legal(play) and self.is_connected(play) and self.is_consecutive(play)
        if valid:
            for loc in play.letters:
                self.letters[loc[0]][loc[1]] = play.letters[loc]
        else:
            raise ValueError("This play is invalid")
        self.update_playable_areas(play, first_play)

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

    def is_valid_play_with_blank(self, play: Play) -> tuple:
        """
        Is the given play with blank tiles a valid play
        :param play: The play who's validity is to be determined
        :return: True if the play is valid, False, otherwise
        """
        blanks = list(play.letters.values()).count("?")
        replacements = generate_blank_replacements(blanks)
        for replacement in replacements:
            new_play = play.copy()
            new_play.replace_blanks(replacement)
            if self.is_valid_play(new_play):
                return True, new_play
        return False, None

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

    def get_letter_multiplier(self, loc: tuple, played: bool) -> int:
        if played:
            return self.squares[loc[0]][loc[1]].get_letter_multiplier()
        return 1

    def get_word_multiplier(self, loc: tuple, played: bool) -> int:
        if played:
            return self.squares[loc[0]][loc[1]].get_word_multiplier()
        return 1

    def get_text_at(self, row: int, col: int) -> str:
        """
        Return either the letter or board marking at that location
        :param row: the row
        :param col: col
        :return: the text at row col
        """
        if self.letters[row][col] != "":
            return self.letters[row][col].upper()
        elif str(self.squares[row][col]) != "  ":
            return str(self.squares[row][col])
        else:
            return ""

    def remove_play(self, play: Play):
        """
        Removes all the letters in the given play from the board
        :return: None
        """
        for pos in play.letters:
            self.letters[pos[0]][pos[1]] = ""

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