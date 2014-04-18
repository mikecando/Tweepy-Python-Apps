"""
This process will stream tweets based on a keyword that is entered
"""

#imports
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import textwrap
 
import tweepy, time, sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open(r'keys.config'))
consumer_key = config.get('key values', 'consumer_key')
consumer_secret = config.get('key values', 'consumer_secret')
access_token = config.get('key values', 'access_token')
access_token_secret = config.get('key values', 'access_token_secret')
 
class TweetListener(StreamListener):
    # A listener handles tweets are the received from the stream.
    #This is a basic listener that just prints received tweets to standard output

    def on_data(self, data):
        print data
        #print textwrap.fill(data.text, width=60, initial_indent='    ', subsequent_indent='    ')
        #print '\n %s  %s  via %s\n' % (data.author.screen_name, data.created_at, data.source)
        return True
 
    def on_error(self, status):
        print status
 
#printing all the tweets to the standard output
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
stream = Stream(auth, TweetListener())
stream.filter(track=['#calvary'])
