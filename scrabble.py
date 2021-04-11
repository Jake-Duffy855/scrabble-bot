import time

merriam_webster_2014 = "merriam_webster.txt"
british_dictionary = "english_dictionary.txt"

dicts = {}
with open(british_dictionary) as d:
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
    if letter != "?":
        return ord(letter.lower()) - 97
    else:
        return 26


def all_length_perms(word: str, first=False):
    return permutations_helper(word, "", first)


def permutations_helper(word: str, ans: str, first=False):
    result = []
    if len(ans) > 0:
        result.append(ans)

    alpha = [True for i in range(27)]

    for i in range(len(word)):
        ch = word[i]
        rest = word[0:i] + word[i + 1:]

        if alpha[char_position(ch)] and (first or is_valid_perm(ans + ch)):
            result.extend(permutations_helper(rest, ans + ch, first))
        alpha[char_position(ch)] = False
    return result


def contains_all_letters(word: str, letters: str):
    word = [char for char in word]
    blanks = 0
    for letter in letters.upper():
        if letter == "?":
            blanks += 1
        else:
            try:
                word.remove(letter)
            except ValueError:
                return False
    return len(word) >= blanks


def words_with_all_letters(letters: str) -> list:
    result = []
    for word in words:
        if contains_all_letters(word, letters):
            result.append(word)
    return result


def substring_in_order(word: str, sub: str) -> bool:
    """
    Does word have all the letters of sub in the order they appear in sub
    :param word: the word to check the contents of
    :param sub: the letters word must contain
    :return: True if word contains all the letters of sub in order, False otherwise
    """
    index = 0
    for char in sub.upper():
        if char == "?":
            index += 1
        else:
            try:
                index = word.index(char, index)
            except ValueError:
                return False
    return True


def get_dict(perm: str):
    code = "".join(sorted(perm))
    if code not in dicts.keys():
        dicts[code] = words_with_all_letters(perm)
    return dicts[code]


def is_valid_perm(perm: str) -> bool:
    """
    Does the given permutation appear in order in any word in the dictionary
    :param perm: the permutation of letters to check
    :param dic: what to check the perms against
    :return: True if the perm is found in order in the dictionary, False otherwise
    """
    to_check = words
    if len(perm) >= 4:
        to_check = get_dict(perm)
    for word in to_check:
        if substring_in_order(word, perm):
            return True
    return False
