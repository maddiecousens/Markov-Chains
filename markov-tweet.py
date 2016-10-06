from random import choice
import sys
import twitter
import os


def setup_twitter():
    """ Returns api object of the twitter Library"""
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


def create_text_string(tweeter_list):
    final_string = ''
    for tweet_list in tweeter_list:
        final_string += ' ' + ' '.join(tweet_list)

    return final_string



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

    # Iterating over the length of all words in the file, not including the last
    # n items (so that last tuple is in range)
    for i in xrange(len(words) - (n - 1)):

        #initialize key that will be tupalized later
        n_gram_key = []

        # Iterate over n within i, so that each time we are making a key of n 
        # words starting at the ith index
        for j in xrange(n):
            n_gram_key.append(words[i + j])

        # If there is a next word in text string assign it to next_word
        if i < len(words) - n:
            next_word = words[i+n]
        # If last work in tuple key is last word in text string (same thing 
            # as words list) then set next_word to None
        else:
            next_word = None

        # If the key already exists, append next word to the value list. 
        # Otherwise, initialize with an empty list and append next_word
        chains.setdefault(tuple(n_gram_key), []).append(next_word)

    return chains

def create_sentence(chains, n):

    # Create list of keys that start with a capitalized word
    # capital_keys = [key for key in chains.keys() if key[0].istitle()]
    
    # Choose random word from capital_keys
    # key = choice(capital_keys)
    key = choice(chains.keys())

    # Create text list initialized with words from key tuple
    text = list(key)

    creating_sentence = True

    while creating_sentence:
        
        # Set next word to random choice from value list at that key
        next_word = choice(chains[key])
        
        # If next word is not None
        if next_word:
            # Add next_word to text list
            text.append(next_word)
            # End creating sentence if next_word ends in punctuation.
            if next_word[-1] in ['.', '!', '?']:
                creating_sentence = False
        # If next_word is None end creating sentence
        else:
            creating_sentence = False

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


def get_twitter_posts(api, username, num_posts = 15):
    tweets = []
    twitter_obj = api.GetUserTimeline(screen_name=username, count=200)
    while len(tweets) < num_posts:
        for tweet in twitter_obj:
            # this excludes tweets with photos
            if not tweet.media:
                tweets.append(tweet.text)
        break
    return tweets
    


api = setup_twitter()

# usernames = ['kanyewest', 'realdonaldtrump']

kanye = get_twitter_posts(api, 'kanyewest',100)
# trump = get_twitter_posts(api, 'realdonaldtrump')
kim = get_twitter_posts(api, 'kimkardashian', 100)
emoji = get_twitter_posts(api, 'emojistory', 100)

input_text = create_text_string([kanye, emoji, kim])

# print input_text
# import pdb; pdb.set_trace()

# print api.VerifyCredentials()
# input_path = sys.argv[1]
n = int(sys.argv[1])

# Open the file and turn it into one long string
# input_text = open_and_read_file(input_path)
# Get a Markov chain
chains = make_chains_n(input_text, n)
tweet =  make_text_n(chains, n)
print tweet

status = api.PostUpdate(tweet)
# print status