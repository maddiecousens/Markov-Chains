from random import choice


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

    for i in xrange(len(words) - 1):
        word1 = words[i]
        word2 = words[i + 1]

        if i < len(words) - 2:
            word3 = words[i + 2]
        else:
            word3 = None

        # if (word1, word2) in chains:
        #     chains[(word1, word2)].append(word3)
        # else:
        #     chains[(word1, word2)] = [word3]

        # get the thing that's at the key (word1, word2), if it doesn't exist, get&set []
        # append word3 to ^
        chains.setdefault((word1, word2), []).append(word3)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    text = ""

    # your code goes here

    return text


input_path = "green-eggs.txt"

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)
print input_text

# Get a Markov chain
chains = make_chains(input_text)
for k, v in chains.iteritems():
    print k, v

# # Produce random text
# random_text = make_text(chains)

# print random_text
