#By: Sohrab Redjai Sani; Feb-2016

#-------- importing necessary libraries
import sys
import tweepy
from tweepy import OAuthHandler
import pymongo
from pymongo import MongoClient
from pymongo import GEO2D

consumer_key= open('consumer_key.txt', 'r').read()
consumer_secret= open('consumer_secret.txt', 'r').read()

access_token= open('access_token.txt', 'r').read()
access_token_secret= open('access_token_secret.txt', 'r').read() 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

         #Creating and Connecting to MongoDB Database: supperbowl
        self.db = pymongo.MongoClient('localhost', 27017).supperbowl


    def on_status(self, status):
        status.text=str(unicode(status.text).encode("utf-8"))
        print status.text , "\n"

        data ={}
        data['text'] = status.text
        data['created_at'] = status.created_at
        data['geo'] = status.geo
        data['source'] = status.source
        data['id'] = status.id


# Identifying in which collection the data should be saved.
        self.db.sbCambridge7.insert(data)


    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
sapi.filter(track=['Super Bowl', 'Carolina Panthers', 'Denver Broncos'])
										#specify your keyword(s)
