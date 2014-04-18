import tweepy, time, sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open(r'keys.config'))
consumer_key = config.get('key values', 'consumer_key')
consumer_secret = config.get('key values', 'consumer_secret')
access_token = config.get('key values', 'access_token')
access_token_secret = config.get('key values', 'access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

public_tweets = api.public_timeline()
for tweet in public_tweets:
    print tweet.text
