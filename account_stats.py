#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys
import ConfigParser

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.readfp(open(r'keys.config'))
    consumer_key = config.get('key values', 'consumer_key')
    consumer_secret = config.get('key values', 'consumer_secret')
    access_token = config.get('key values', 'access_token')
    access_token_secret = config.get('key values', 'access_token_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print 'Getting statistics for @GlorifyHimNow:'

    # Get information about the user
    data = api.get_user('GlorifyHimNow')

    print 'Followers: ' + str(data.followers_count)
    print 'Tweets: ' + str(data.statuses_count)
    print 'Favouries: ' + str(data.favourites_count)
    print 'Friends: ' + str(data.friends_count)
    print 'Appears on ' + str(data.listed_count) + ' lists'

    """
    #now get the latest trends
    US_WOE_ID = 23424977
    us_trends = api.trends.place(_id=US_WOE_ID)
    trend = set([trend['name']
                    for trend in us_trends[0]['trends']])
    rank = 0
    for j in trend:
        rank += 1
        print str(rank) + '   ' + j
    """


