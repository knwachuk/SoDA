'''
This is the Twitter API to do all of the data acquisition.
'''

from __future__ import print_function

import json
import csv
import sys
import tweepy

#class TwitterAPI(tweepy.streaming.StreamListener):
class TwitterAPI(tweepy.StreamListener):
    '''
    This is the DEPA TwitterAPI version 2. Written in Python 2.7.
    '''

    def __init__(self, user_credentials=None):
        self.credentials = user_credentials

    # Getting user information
    def get_user_info_csv(self, filename):
        '''
        '''
        user_info = {}
        try:
            with open(filename, 'r') as fp:
                reader = csv.reader(fp)
                for row in reader:
                    user_info['consumer_key'] = row[0]
                    user_info['consumer_secret'] = row[1]
                    user_info['access_token'] = row[2]
                    user_info['access_token_secret'] = row[3]
                return user_info
        except IOError as e:
            print(e)
            filename = raw_input("Please enter a new file name: ")
            self.get_user_info_csv(filename)

    def get_user_info_json(self, filename):
        '''
        '''
        try:
            with open(filename, 'r') as fp:
                self.credentials = json.load(fp)
        except IOError as e:
            print(e)
            filename = raw_input("Please enter a new user file name: ")
            self.get_user_info_json(filename)

class StdOutListener(tweepy.StreamListener):
    '''
    This is the basic listener that just prints received tweets to stdout.
    '''
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)
        return True # Don't kill the stream
        #print("Stream restarted")


def main():

    api = TwitterAPI()
    listener = StdOutListener()

    #api.get_user_info_json('twitter-credentials.json')
    api.get_user_info_json('/Users/kelechi/Dropbox/Research_Central/EVRL/social_data_analytics/api/twitter/twitter-credentials.json')

    auth = tweepy.OAuthHandler(api.credentials['consumer_key'],
                               api.credentials['consumer_secret'])
    auth.set_access_token(api.credentials['access_token'],
                          api.credentials['access_token_secret'])
    stream = tweepy.Stream(auth, listener)

    # This line filter Twitter Streams to capture data by the keywords:
    # 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])


if __name__ == '__main__':
    main()
