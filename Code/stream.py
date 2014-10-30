from twitter import *
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
ACC_TOKEN = '152187124-8ih3pnzeyAqlvQNKKs5nDRHjfVHyugoABXOk4Gf4'
ACC_SECRET = 'xOyvSkIcqijdA93RMTcIxZu3Bma3arhlTNThMYVkZq058'
CON_KEY = 'mf4fvrM8rwSQskzt3ITkHMCCU'
CON_SECRET = '3Q0oJa8Xi9N8jZBFVXs4KxeR0Q3lkVu38KvHJ00DkSbY9Bq2xu'

#t = Twitter(auth=OAuth(acc_token,acc_secret,con_key,con_secret))

class listener(StreamListener):

    def on_data(self, data):
        data = self.convert_to_utf(json.loads(data))
        print data["text"]
        return True

    def on_error(self, status):
        print status


    def convert_to_utf(self, input):
        if isinstance(input, dict):
            temp_dict = {}
            for key,value in input.iteritems():
                temp_dict[self.convert_to_utf(key)] = self.convert_to_utf(value)
            return temp_dict
            #return {self.convert_to_utf(key): self.convert_to_utf(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            temp_list = []
            for element in input:
                temp_list.append(self.convert_to_utf(element))
            return temp_list
            #return [self.convert_to_utf(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input


auth = OAuthHandler(CON_KEY, CON_SECRET)
auth.set_access_token(ACC_TOKEN, ACC_SECRET)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["#irony"])
