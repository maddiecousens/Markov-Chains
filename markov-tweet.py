from random import choice
import sys
import twitter
import os


def setup_twitter():
    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    return api


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    with open(file_path) as textfile:
        text = textfile.read()

    return text


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

def create_sentence(chains, n):

    capital_keys = [key for key in chains.keys() if key[0].istitle()]
    # starting_key = choice(capital_keys)
    key = choice(capital_keys)

    text = list(key)
    # text = list(starting_key)
    # text = []
    # for i in xrange(n):
    #     text.append(starting_key[i])

    while True:
        # key_check = []
        # for j in xrange(-n, 0):
        #     key_check.append(text[j])

        # next_word = choice(chains[tuple(key_check)])
        
        next_word = choice(chains[key])
        
        if next_word:
            # only if next word is not None
            text.append(next_word)
            # end if reaches end of punctuation
            if next_word[-1] in ['.', '!', '?']:
                break
        # next_word is None
        else:
            break

        key = key[1:] + (next_word,)

    return " ".join(text)


def make_text_n(chains, n):
    """Takes dictionary of markov chains; returns random text."""


    MAX_CHARS = 140
    sentences_list = []
    composing_tweet = True

    while composing_tweet:
        new_sentence = create_sentence(chains, n)
        # check if length of current setnecnes and new sentence is less than 140
        if len(" ".join(sentences_list)) + len(new_sentence) < MAX_CHARS:
            sentences_list.append(new_sentence)
        # if it is too long, chekc if anything is in sentences list at all
        elif sentences_list:
            # if we have stuff in the setnences list, we have something to post
            composing_tweet = False

    return " ".join(sentences_list)


api = setup_twitter()

# import pdb; pdb.set_trace()

# print api.VerifyCredentials()
input_path = sys.argv[1]
n = int(sys.argv[2])

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)
# Get a Markov chain
chains = make_chains_n(input_text, n)
tweet =  make_text_n(chains, n)
print tweet

status = api.PostUpdate(tweet)
# print status