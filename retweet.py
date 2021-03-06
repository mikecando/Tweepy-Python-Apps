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
import zmq


logging.basicConfig(filename='retweet.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%d %b %Y %H:%M:%S.%p')

screenNames = ['MaxLucado', 'TimTebow', 'JohnPiper', 'BishopJakes', 'RaviZacharias','plattdavid', 'FrankViola',
               'LeeStrobel', 'JeffersonBethke', 'RickWarren', 'ChristianPost','MattWalshRadio', 'desiringgod',
               'CSLewisDaily', 'kilmeade', 'TGC']

def ProcessIsNotAlreadyRunning():
    ctx = zmq.Context()
    s = ctx.socket(zmq.SUB)
    s.connect("tcp://127.0.0.1:5568")
    s.setsockopt(zmq.SUBSCRIBE,'')
    poller = zmq.Poller()
    poller.register(s, zmq.POLLIN) # POLLIN for recv, POLLOUT for send
    print 'Checking is the process is already running'
    #msg = s.recv()
    evts = poller.poll(30000) # wait *up to* one second for a message to arrive.
    if(len(evts) < 1):
        return True
    else:
        return False

def getRandomSleepTime(min,max):
    return random.randrange(min,max)

def runRetweet():
    logging.info('*****  Process started  **********')
    config = ConfigParser.ConfigParser()
    config.readfp(open(r'keys.config'))
    consumer_key = config.get('key values', 'consumer_key')
    consumer_secret = config.get('key values', 'consumer_secret')
    access_token = config.get('key values', 'access_token')
    access_token_secret = config.get('key values', 'access_token_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

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
            while(sleepTime > 0):
                time.sleep(5)
                s.send('Running')
                sleepTime -= 5
        except Exception, e:
            logging.error('exception: ' + str(e))
            errorTime = 60
            while(errorTime > 0):
                time.sleep(5) # sleep for 60 seconds on an error
                s.send('Running')
                errorTime -= 5

if __name__ == "__main__":
    if ProcessIsNotAlreadyRunning():
        print 'Process is not running.......'
        print 'Starting now.............'
        ctx = zmq.Context()
        s = ctx.socket(zmq.PUB)
        s.bind("tcp://*:5568")
        runRetweet()
    else:
        print 'Process already running....'
        print 'Exiting..............'