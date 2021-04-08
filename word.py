class Word:
    """Represent a word on the board"""

    def __init__(self, letters: dict, played: dict):
        self.letters = letters
        self.played = played
        self.word = self.get_word()

    def get_word(self):
        result = ""
        for loc in sorted(self.letters):
            result += self.letters[loc]
        return result

    # def is_valid(self):
