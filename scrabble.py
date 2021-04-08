import time

with open("dictionary.txt") as d:
    words = d.read()
    words = words.split()
    words = dict.fromkeys(words, True)

values = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
          "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
          "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
          "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
          "x": 8, "z": 10, "?": 0}


def is_valid(word: str) -> bool:
    """
    Is the given word a valid scrabble word?
    :param word: The word whose validity is to be determined
    :return: True if the word is valid, False otherwise
    :rtype: bool
    """
    return words.get(word.upper(), False)


def binary_search(word: str, left=0, right=len(words)):
    if right - left < 2:
        return False

    mid = int((left + right) / 2)
    if words[mid] == word:
        return True
    elif words[mid] > word:
        return binary_search(word, left, mid)
    else:
        return binary_search(word, mid, right)


def score_word(word: str):
    """
    Returns the score of the given word, 0 if invalid
    :param word: the word to be scored
    :return: the score of the word, 0 if invalid
    :rtype: int
    """
    if is_valid(word):
        score = 0
        for c in word:
            score += values[c]
        return score
    else:
        return 0


def char_position(letter):
    return ord(letter) - 97


def all_length_perms(word: str):
    result = []
    for i in range(len(word)):
        result.extend(permutations_helper(word, "", i))
    return result


def permutations(word: str):
    permutations_helper(word, "", 0)


def permutations_helper(word: str, ans: str, left: int):
    result = []
    if len(word) == left:
        result.append(ans)

    alpha = [True for i in range(26)]

    for i in range(len(word)):
        ch = word[i]
        rest = word[0:i] + word[i + 1:]

        if alpha[char_position(ch)]:
            result.extend(permutations_helper(rest, ans + ch, left))
        alpha[char_position(ch)] = False
    return result
