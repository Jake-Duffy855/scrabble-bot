from scrabble import is_valid
from squares import *
from play import *


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

    def get_best_play(self, letters: list) -> Play:
        """
        Returns the highest score play possible with the given letters
        :param letters: The list of letters that are able to be played
        :return: The play with the highest score using the given letters
        """
        pass

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
        result = set()
        for loc in sorted(play.letters.keys()):
            word = self.get_vertical_word(play.letters[loc], loc, play.letters)
            if len(word) > 1:
                result.add(word)
            word = self.get_horizontal_word(play.letters[loc], loc, play.letters)
            if len(word) > 1:
                result.add(word)
        print(result)
        return result

    def is_connected(self, play: Play) -> bool:
        """
        Does the given Play connect to present words or is it the first word
        :param play: the play to determine
        :return: True if connected, False is not
        """
        if self.letters == [["" for i in range(15)] for j in range(15)]:
            return True

        for loc in play.letters:
            try:
                if self.letters[loc[0] + 1][loc[1]] != "":
                    return True
                elif self.letters[loc[0] - 1][loc[1]] != "":
                    return True
                elif self.letters[loc[0]][loc[1] + 1] != "":
                    return True
                elif self.letters[loc[0]][loc[1] - 1] != "":
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
            if not is_valid(word):
                print(word)
                return False
        return self.is_legal(play) and self.is_connected(play) and self.is_consecutive(play)

    def get_vertical_word(self, letter, loc, letters: dict):
        word = letter
        x = loc[0]
        y = loc[1]
        while x > 0 and (self.letters[x - 1][y] or (x - 1, y) in letters):
            if self.letters[x - 1][y]:
                word = self.letters[x - 1][y] + word
            else:
                word = letters[x - 1, y] + word
            x -= 1
        x = loc[0]
        while x < 14 and (self.letters[x + 1][y] or (x + 1, y) in letters):
            if self.letters[x + 1][y]:
                word = word + self.letters[x + 1][y]
            else:
                word = word + letters[x + 1, y]
            x += 1
        return word

    def get_horizontal_word(self, letter, loc, letters: dict):
        word = letter
        x = loc[0]
        y = loc[1]
        while y > 0 and (self.letters[x][y - 1] or (x, y - 1) in letters):
            if self.letters[x][y - 1]:
                word = self.letters[x][y - 1] + word
            else:
                word = letters[x, y - 1] + word
            y -= 1
        y = loc[1]
        while y < 14 and (self.letters[x][y + 1] or (x, y + 1) in letters):
            if self.letters[x][y + 1]:
                word = word + self.letters[x][y + 1]
            else:
                word = word + letters[x, y + 1]
            y += 1
        return word

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
        (7, 7): "a",
        (7, 8): "p",
        (7, 9): "p",
        (7, 10): "l",
        (7, 11): "e",
    }))
    my_board.play(Play({
        (8, 7): "n",
    }))
    my_board.play(Play({
        (8, 8): "o",
        (9, 8): "l",
        (10, 8): "i",
        (11, 8): "s",
        (12, 8): "h",
    }))
    my_board.play(Play({
        (12, 9): "e",
        (12, 10): "l",
        (12, 11): "l",
    }))
    print(my_board)
