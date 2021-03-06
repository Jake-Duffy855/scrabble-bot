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

    def replace_blanks(self, replacements: list):
        blank = 0
        for loc in self.letters:
            if self.letters[loc] == "?":
                try:
                    self.letters[loc] = replacements[blank]
                    blank += 1
                except Exception:
                    raise ValueError("Dimension mismatch between blanks and replacements")

    def copy(self):
        return Play(self.letters.copy())

    def __str__(self):
        result = "my_board.play(Play({\n"
        for key in self.letters:
            result += str(key) + ": \"" + self.letters[key] + "\",\n"
        return result[:-2] + "}))"
