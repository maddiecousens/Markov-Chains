from random import choice
import sys


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    with open(file_path) as textfile:
        text = textfile.read()

    return text


def make_chains(text_string):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    words = text_string.split()

    #  Loops through words, creates dictionary with tuples as keys and values of
    #       lists of possible next words
    for i in xrange(len(words) - 1):
        word1 = words[i]
        word2 = words[i + 1]

        if i < len(words) - 2:
            word3 = words[i + 2]
        else:
            word3 = None
            # If tuple exists as key, add next word to value list.
            # If tuple does not exist as key, add to dictionary initialized with
            #   empty list and append next word
        chains.setdefault((word1, word2), []).append(word3)
        
    return chains

def make_chains_n(text_string, n):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of n values
    and the value would be a list of the word(s) that follow those n
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    words = text_string.split()

    for i in xrange(len(words) - (n - 1)):
        n_gram_key = []
        for j in xrange(n):
            n_gram_key.append(words[i + j])

        if i < len(words) - n:
            next_word = words[i+n]
        else:
            next_word = None

        chains.setdefault(tuple(n_gram_key), []).append(next_word)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    # Randomly choose key from dictionary which will be a tuple
    starting_key = choice(chains.keys()) 

    # Create list of words, starting with values from starting_key tuple
    text = [starting_key[0], starting_key[1]]

    # While last two values of list exist as tuple key in chains dictionary,
    #       choose next word from values at that key and append to words list
    # while (text[-2], text[-1]) in chains:
    while True:
        next_word = choice(chains[(text[-2], text[-1])])
        if next_word:
            text.append(next_word)
        else:
            break

    # Join list, return string
    return " ".join(text)


def make_text_n(chains, n, sentences):
    """Takes dictionary of markov chains; returns random text."""

    # Randomly choose key from dictionary which will be a tuple

    capital_keys = [key for key in chains.keys() if key[0].istitle()]
    starting_key = choice(capital_keys)

    text = []
    count = 0
    for i in xrange(n):
        text.append(starting_key[i])

    while True and count < sentences:
        key_check = []
        for j in xrange(-n, 0):
            key_check.append(text[j])
        next_word = choice(chains[tuple(key_check)])

        if next_word:
            text.append(next_word)
            # if not next_word[-1].isalpha() and not next_word[-1].isdigit():
            if next_word[-1] in ['.', '!', '?']:
                count += 1
        else:
            break

    return " ".join(text)


input_path = sys.argv[1]
n = int(sys.argv[2])
sentences = int(sys.argv[3])

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)


# Get a Markov chain
chains = make_chains_n(input_text, n)
# print chains

# # Produce random text
random_text = make_text_n(chains, n, sentences)


print random_text
