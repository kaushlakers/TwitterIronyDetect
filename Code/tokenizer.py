from nltk import corpus
import urlparse
from twokenize import *
from FileOperations import *


HASHTAGS = ['irony','ironic','.',':','?','0','|',',','...','\"',"irony#","rt"]

def tokenize_data(tweets):
    tokenized_cleaned_tweets = []
    for tweet in tweets:
        cleaned_tweet = remove_hashtags(tweet)
        tokenized_tweet = FileOperations.convert_to_utf(tokenize(cleaned_tweet))
        tokenized_tweet = get_words_after_stop_word_removal(tokenized_tweet)
        tokenized_tweet = [token for token in tokenized_tweet if token.lower() not in HASHTAGS]
        tokenized_cleaned_tweets.append(tokenized_tweet)
    return tokenized_cleaned_tweets
        #self.tweet_words.extend(tokenized_tweet)

def tokenize_single_tweet(tweet):
    cleaned_tweet = remove_hashtags(tweet)
    tokenized_tweet = FileOperations.convert_to_utf(tokenize(cleaned_tweet))
    tokenized_tweet = get_words_after_stop_word_removal(tokenized_tweet)
    tokenized_tweet = [token for token in tokenized_tweet if token.lower() not in HASHTAGS]
    return tokenized_tweet

def get_words_after_stop_word_removal(tokens):
    good_words = [w for w in tokens if w.lower() not in corpus.stopwords.words('english')]
    return good_words

def remove_hashtags(tweet):
    cleaned_tweet = ''
    for i in tweet.split():
        s, n, p, pa, q, f = urlparse.urlparse(i)
        if s and n:
            pass
        elif i[:1] == '.':
            pass
        elif i[:1] == '#' or i[:1]=='@':
            cleaned_tweet = cleaned_tweet.strip() + ' ' + i[1:]
        else:
            cleaned_tweet = cleaned_tweet.strip() + ' ' + i
    return cleaned_tweet
