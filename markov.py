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
            # If tuple exists as key, add next word to value list.
            # If tuple does not exist as key, add to dictionary initialized with
            #   empty list and append next word
            chains.setdefault((word1, word2), []).append(word3)
        
    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    # Randomly choose key from dictionary which will be a tuple
    starting_key = choice(chains.keys()) 

    # Create list of words, starting with values from starting_key tuple
    text = [starting_key[0], starting_key[1]]

    # While last two values of list exist as tuple key in chains dictionary,
    #       choose next word from values at that key and append to words list
    while (text[-2], text[-1]) in chains:
        text.append(choice(chains[(text[-2], text[-1])]))

    # Join list, return string
    return " ".join(text)


input_path = sys.argv[1]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)


# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)


print random_text
