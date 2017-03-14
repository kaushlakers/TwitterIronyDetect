import json
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from oauthhelper import *
from nltk.collocations import *
import nltk
from nltk.tokenize import word_tokenize
class Search:
    def __init__(self, auth):
        self.auth = auth
        self.results = []

    def query_and_save(self, query):
        api = tweepy.API(self.auth)
        search_results = api.search(q=query, count=10000)
        for tweet in search_results:
            self.results.append(nltk.word_tokenize(tweet.text))
        filename = query.replace(' ','_')
        fp = open(filename+".twts","w")
        json.dump(self.results, fp, indent=4)
        fp.close()

def main():
    search = Search(OAuthHelper.get_auth())
    search.query_and_save('#irony')

if __name__ == "__main__": main()
