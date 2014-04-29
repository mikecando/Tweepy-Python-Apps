from urllib2 import urlopen
import re
import tweepy, time, sys
import ConfigParser
import random
import logging
import os
import zmq

def ProcessIsNotAlreadyRunning():
    ctx = zmq.Context()
    s = ctx.socket(zmq.SUB)
    s.connect("tcp://127.0.0.1:5567")
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

logging.basicConfig(filename='tweet_bible_verse.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%d %b %Y %H:%M:%S.%p')



#List of words to hashtag
hashTags = [ 'amazingword', 'Passover', 'father', 'Easter', 'scripture', 'theology', 'TheGospel',
                'lastdays', 'rapture', 'EndOfTheWorld', 'Millennium', 'TWorship', 'apologetics', 'jesustweeters',
                'teamjesus', 'prophecy', 'apocalypse', 'apologists', 'EndTimes', 'EndofDays', 'armageddon',
                'bible', 'prayer', 'pray', 'faith', 'keepfaith', 'Scripture', 'eschatology', 'messianic',
                'hebrewchristian', 'Hannukkah', 'chanukah', 'judaism', 'torah', 'Jews', 'jewish', 'Israel',
                'Christian', 'Agnostics', 'Christianity', 'Religious', 'Religion', 'God', 'Jesus', 'spiritual',
                'Oldtestament', 'NewTestament', 'ascended', 'Jerusalem', 'ascension', 'Sabbath', 'atheism',
                'atheist', 'skeptic', 'anarchist', 'antiChrist', 'Apostasy', 'Biblical', 'Christians', 'FalseProphet ',
                'hades', 'hell', 'NewWorldOrder', 'nwo', 'OIC', 'Pope', 'satan', 'sioa', 'tcot',
                'ThousandYearMillineum', 'Tribulation', 'Vatican', 'markofthebeast', 'ConversationWithGod',
                'GodLovesYou', 'HearingGod', 'peace', 'love', 'father' ]

"""
This function will return a random bible verse. It will also remove any
unwanted sequence of characters such as <b>,</b>,&#8211,....
It will also add hashtags based on the hasgTags list of words
"""
def randomVerse():
    url = "http://labs.bible.org/api/?passage=random"
    response = urlopen(url)
    raw_data = response.read().decode('utf-8')
    #remove any unwanted sequence of characters from the returned text
    raw_data = re.sub('<b>', '', raw_data)
    raw_data = re.sub('</b>', '', raw_data)
    raw_data = re.sub('&#8211', '', raw_data)
    #add hashtags where applicable
    for item in hashTags:
        raw_data = re.sub("(?i)" + item,'#' + item, raw_data)
    return raw_data

def getRandomSleepTime(min,max):
    return random.randrange(min,max)

def runTweetBibleVerse():
    config = ConfigParser.ConfigParser()
    config.readfp(open(r'keys.config'))
    consumer_key = config.get('key values', 'consumer_key')
    consumer_secret = config.get('key values', 'consumer_secret')
    access_token = config.get('key values', 'access_token')
    access_token_secret = config.get('key values', 'access_token_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    #collected for statistics
    hashTaggedVerses = 0
    totalVersesSent = 0
    percentOfhashTaggedVerses = 0
    totalVersesLessThan140Chars = 0
    totalVersesRetrieved = 0
    percentOfVersesLessThan140Chars = 0

    while True:
        try:
            verse = randomVerse()
            totalVersesRetrieved += 1
            verseLen = len(verse)
            logging.debug('verse is: ' + verse)
            logging.debug('Verse length = ' + str(verseLen))
            if verseLen <= 140:
                api.update_status(verse)
                totalVersesLessThan140Chars += 1
                totalVersesSent += 1
                hashTagCount = len(re.findall("#", verse))
                if(hashTagCount > 0):
                    hashTaggedVerses += 1
                    logging.debug('New verse has hashTags. count = ' + str(hashTagCount))
                else:
                    logging.debug('New verse does not have hashTags!!!')

                #Get the statistics for how many verses were < 140 chars
                percentOfVersesLessThan140Chars = (totalVersesLessThan140Chars/float(totalVersesRetrieved)) * 100
                logging.info(str(totalVersesLessThan140Chars) + ' out of ' + str(totalVersesRetrieved) + ' verses are < 140 chars = ' +
                             "{:5.2f}".format(percentOfVersesLessThan140Chars) + '%')

                #Get the statistics for how many verse < 140 chars had hash tags
                percentOfhashTaggedVerses = (hashTaggedVerses/float(totalVersesSent)) * 100
                logging.info(str(hashTaggedVerses) + ' out of ' + str(totalVersesSent) + ' verses are hash tagged = ' +
                             "{:5.2f}".format(percentOfhashTaggedVerses) + '%')

                #Get a random sleep time between a min and max seconds
                sleepTime = getRandomSleepTime(300,1200)
                logging.info('Next tweet to be sent in ' + str(sleepTime) + ' seconds')
                while(sleepTime > 0):
                    time.sleep(5)
                    s.send('Running')
                    sleepTime -= 5
            else:
                logging.debug('Tweet is ' + str(verseLen) + ' characters and is too long!!!')
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
        s.bind("tcp://*:5567")
        logging.info('*****  Process started  **********')
        runTweetBibleVerse()
    else:
        print 'Process already running....'
        print 'Exiting..............'
