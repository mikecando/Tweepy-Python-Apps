from urllib2 import urlopen
import re
import twitter, time, sys
import ConfigParser
import random
import logging
import os
import datetime
import csv

logging.basicConfig(filename='tweet_bible_verse.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%d %b %Y %H:%M:%S.%p')

config = ConfigParser.ConfigParser()
config.readfp(open(r'keys.config'))
consumer_key = config.get('key values', 'consumer_key')
consumer_secret = config.get('key values', 'consumer_secret')
access_token = config.get('key values', 'access_token')
access_token_secret = config.get('key values', 'access_token_secret')

auth = twitter.oauth.OAuth(access_token, access_token_secret,
                           consumer_key, consumer_secret)

api = twitter.Twitter(auth=auth)

trend = set([])

def getTrends():
    # The Yahoo! Where On Earth ID for the entire world is 1.
    # See https://dev.twitter.com/docs/api/1.1/get/trends/place and
    # http://developer.yahoo.com/geo/geoplanet/

    WORLD_WOE_ID = 1
    US_WOE_ID = 23424977

    # Prefix ID with the underscore for query string parameterization.
    # Without the underscore, the twitter package appends the ID value
    # to the URL itself as a special case keyword argument.

    #world_trends = api.trends.place(_id=WORLD_WOE_ID)
    us_trends = api.trends.place(_id=US_WOE_ID)

    trend = set([trend['name']
                         for trend in us_trends[0]['trends']])

    return trend
sampleNumber = 0
while True:
    try:
        trend = getTrends()
        i = datetime.datetime.now()
        with open('trendData4.csv', 'ab') as outfile:
            w = csv.writer(outfile, delimiter=',')
            rank = 0
            sampleNumber += 1
            for j in trend:
                rank += 1
                w.writerow([sampleNumber,i.strftime('%Y/%m/%d %H:%M:%S'),rank,j])
            outfile.close()
        time.sleep(300)
    except Exception, e:
        print 'exception: ' + str(e)
        time.sleep(120) # sleep for 60 seconds on an error

