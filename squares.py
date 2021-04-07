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