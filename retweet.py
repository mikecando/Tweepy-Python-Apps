#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This process has a list of screen names and randomly
"""

import tweepy
import os
import ConfigParser
import inspect
import random
import logging
import time

logging.basicConfig(filename='retweet.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%d %b %Y %H:%M:%S.%p')

logging.info('*****  Process started  **********')

def getRandomSleepTime(min,max):
    return random.randrange(min,max)

config = ConfigParser.ConfigParser()
config.readfp(open(r'keys.config'))
consumer_key = config.get('key values', 'consumer_key')
consumer_secret = config.get('key values', 'consumer_secret')
access_token = config.get('key values', 'access_token')
access_token_secret = config.get('key values', 'access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

screenNames = ['MaxLucado', 'TimTebow', 'JohnPiper', 'BishopJakes', 'RaviZacharias','plattdavid', 'FrankViola',
               'LeeStrobel', 'JeffersonBethke', 'RickWarren', 'ChristianPost','MattWalshRadio', 'desiringgod',
               'CSLewisDaily', 'kilmeade', 'TGC']

while True:
    try:
        screenNameIndex = random.randrange(0,9)
        logging.info('Random screen name index is ' + str(screenNameIndex) + ' which is user ' + screenNames[screenNameIndex])
        retweetIndex = random.randrange(0,99)
        logging.info('Random retweet index is ' + str(retweetIndex))
        retweet = api.user_timeline(screenNames[screenNameIndex], include_rts=True, count=100)[retweetIndex]
        logging.info('retweet text is: ' + retweet.text)
        results = api.retweet(retweet.id)
        logging.info('Successfully retweeted tweet')
        #Get a random sleep time between a min and max seconds
        sleepTime = getRandomSleepTime(300,1200)
        logging.info('Next retweet to be sent in ' + str(sleepTime) + ' seconds')
        time.sleep(sleepTime)
    except Exception, e:
        logging.error('exception: ' + str(e))
        time.sleep(60) # sleep for 60 seconds on an error