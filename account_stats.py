#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys
import ConfigParser
import smtplib



if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.readfp(open(r'keys.config'))
    consumer_key = config.get('key values', 'consumer_key')
    consumer_secret = config.get('key values', 'consumer_secret')
    access_token = config.get('key values', 'access_token')
    access_token_secret = config.get('key values', 'access_token_secret')

    from_email = config.get('text send', 'from_email')
    from_email_password = config.get('text send', 'from_email_password')
    to_account = config.get('text send', 'to_account')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print 'Getting statistics for @GlorifyHimNow:'

    # Get information about the user
    data = api.get_user('GlorifyHimNow')

    message = 'Followers: ' + str(data.followers_count)
    message += ' , Tweets: ' + str(data.statuses_count)
    message += ' , Favourites: ' + str(data.favourites_count)
    message +=  ' , Friends: ' + str(data.friends_count)
    message +=  ' , Appears on ' + str(data.listed_count) + ' lists'


    msg = """From: %s
    To: %s
    Subject: text-message
    %s""" % (from_email, to_account, message)

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(from_email,from_email_password)
    server.sendmail(from_email, to_account, msg)
    server.quit()



