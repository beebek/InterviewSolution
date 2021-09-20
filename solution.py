from math import sqrt
from pprint import pprint


MATRIX_SIZE = 36
COLUMNS = int(sqrt(MATRIX_SIZE))
INPUT_FILE = "input.txt"
WORD_LIST_FILE = "wordlist.txt"


class Trie:
    """Simple Trie structure for searching words"""

    def __init__(self):
        self.root = {"*": "*"}

    def add_word(self, word):
        """Add word to trie structure"""
        current_node = self.root
        for letter in word:
            if letter not in current_node:
                current_node[letter] = {}
            current_node = current_node[letter]
        current_node["*"] = "*"

    def has(self, word):
        """Check trie structure has the word"""
        current_node = self.root
        for letter in word:
            if letter not in current_node:
                return False
            current_node = current_node[letter]
        return "*" in current_node


class GameBoard:
    def __init__(self):
        self._computed_words = []
        self._game_board_data = []
        self._diagonal_mappings = []
        self._wordlist = None
        self._file_content = None
        self._trie = None

        with open(INPUT_FILE, "r") as f:
            self._file_content = f.read()

        with open(WORD_LIST_FILE, "r") as wl:
            self._wordlist = wl.read().splitlines()

        self.generate_game_board()

        # Add words to Trie structure
        self._trie = Trie()
        for word in self._wordlist:
            self._trie.add_word(word)

    def extract_words(self, letters):
        """Extract words from a list of letters"""
        computed_words = []
        for i, n in enumerate(letters):
            word = n
            computed_words.append(word)
            for j in letters[i + 1 : :]:
                word += j
                computed_words.append(word)
        return computed_words

    def extract_horizontal_words(self, letters):
        """Extract horizontal words"""
        self._computed_words.extend(self.extract_words(letters))

    def extract_vertical_words(self):
        """Extract vertical words"""
        vertical_letters = [[] for i in range(COLUMNS)]
        for row in self.game_board:
            for i, item in enumerate(row):
                vertical_letters[i].append(item)

        for letters in vertical_letters:
            self._computed_words.extend(self.extract_words(letters))

    def extract_diagonal_words(self):
        """Extract diagonal words"""

        self.find_diagonal_mappings()

        diagonal_letters = []
        for diagonal in self._diagonal_mappings:
            words = []
            for d in diagonal:
                for array, index in d.items():
                    words.append(self._game_board_data[array][index])
            diagonal_letters.append(words)

        for letters in diagonal_letters:
            self._computed_words.extend(self.extract_words(letters))

    def generate_game_board(self):
        """Helper function to generate game board data as a matrix"""
        start, end = 0, COLUMNS
        while end <= MATRIX_SIZE:
            letters = self._file_content[start:end]
            self._game_board_data.append([i for i in letters])
            self.extract_horizontal_words(letters)
            start = end
            end += COLUMNS

        self.extract_diagonal_words()
        self.extract_vertical_words()

    def find_diagonal_mappings(self):
        """Map index of row vs the diagonal element in the matrix

        The diagonal elements are extracted as a key value pair
        where:
           key represents matrix row
           value represents index of element in the same matrix row
        """
        diagonals = []
        index = 0
        for i in range(COLUMNS - 1, -1, -1):
            tmp = index
            elements = []
            for j in range(0, i + 1):
                elements.append({tmp: j})
                tmp += 1
            index += 1
            diagonals.append(elements)

        for i in range(1, COLUMNS):
            index = 0
            elements = []
            for j in range(i, COLUMNS):
                elements.append({index: j})
                index += 1
            diagonals.append(elements)
        self._diagonal_mappings = diagonals

    @property
    def game_board(self):
        """Return game board data in a matrix as a list of lists"""
        return self._game_board_data

    @property
    def computed_words(self):
        return self._computed_words

    def extract_valid_words(self):
        """Brute force check using 'in' operator"""
        words = []
        for word in self._computed_words:
            if word in self._wordlist:
                words.append(word)
        pprint(words)

    def extract_valid_words_using_trie(self):
        """Implemented using Trie"""
        words = []
        for word in self._computed_words:
            if self._trie.has(word):
                words.append(word)
        pprint(words)


if __name__ == "__main__":
    g = GameBoard()
    pprint(g.game_board)
    g.extract_valid_words_using_trie()
