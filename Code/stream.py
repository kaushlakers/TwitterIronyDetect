from twitter import *
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
ACC_TOKEN = ''
ACC_SECRET = ''
CON_KEY = ''
CON_SECRET = ''

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
        elif isinstance(input, list):
            temp_list = []
            for element in input:
                temp_list.append(self.convert_to_utf(element))
            return temp_list
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input


auth = OAuthHandler(CON_KEY, CON_SECRET)
auth.set_access_token(ACC_TOKEN, ACC_SECRET)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["#irony"])
