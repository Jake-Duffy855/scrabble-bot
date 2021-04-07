from scrabble import is_valid

double_letters = [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0,), (3, 7), (3, 14), (6, 2), (6, 6), (6, 8), (6, 12), (7, 3),
                  (7, 11), (14, 3), (14, 11), (12, 6), (12, 8), (11, 0,), (11, 7), (11, 14), (8, 2), (8, 6), (8, 8),
                  (8, 12)]
triple_letters = [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9)]
double_words = [(7, 7), (1, 1), (2, 2), (3, 3), (4, 4), (1, 13), (2, 12), (3, 11), (4, 10), (13, 1), (12, 2), (11, 3),
                (10, 4), (13, 13), (12, 12), (11, 11), (10, 10)]
triples_words = [(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)]


class Square:
    """Represent one square in the scrabble board"""

    def __init__(self):
        pass

    def __str__(self):
        return "  "


class DoubleLetter(Square):
    """double"""

    def __str__(self):
        return "DL"


class TripleLetter(Square):
    """triple"""

    def __str__(self):
        return "TL"


class DoubleWord(Square):
    """dobuleword"""

    def __str__(self):
        return "DW"


class TripleWord(Square):
    """tRokafd"""

    def __str__(self):
        return "TW"

# -------------------------------------------------------------------------------------------------------------------


class Play:
    """Represent a play on the board"""

    def __init__(self, letters: dict):
        self.letters = letters
        if not (0 < len(letters) <= 7):
            raise ValueError("Play is not of valid size")
        for loc in letters:
            if not (0 <= loc[0] <= 14) or not (0 <= loc[1] <= 14):
                raise ValueError("Letter location is out of bounds")
        if not self.same_xs() and not self.same_ys():
            raise ValueError("Play must be in a straight line")

    def same_xs(self):
        x = list(self.letters.keys())[0][0]
        for loc in self.letters:
            if loc[0] != x:
                return False
        return True

    def same_ys(self):
        y = list(self.letters.keys())[0][1]
        for loc in self.letters:
            if loc[1] != y:
                return False
        return True

# -------------------------------------------------------------------------------------------------------------------


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
        result = []
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
                return False
        return self.is_legal(play) and self.is_connected(play) and self.is_consecutive(play)

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
        (9, 7): "t"
    }))
    print(my_board)
