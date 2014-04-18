#!/usr/bin/env python
 
"""
Tweepy library proof of concept
 
@author: Adrian Deccico
"""
 
from getpass import getpass
import hashlib
import time
import re
import operator
import logging
import codecs
import tweepy
 
logging.basicConfig(level = logging.INFO)
 
class TweetListener(tweepy.StreamListener):
 
    #we use this pattern to decide if a post is a retweet or not, given that retweet fields of the feed don't work
    __retweet_pattern = "^(rt|retweet).*$"
 
 
    #statistics
    count = 0
    found = 0
    hour_ranking = {}
    retweets = {}
 
    #constants
    TOP_TWEETS = 20 #number of tweets to display in each hour
 
 
    def on_status(self, status):
        """callback that will process new tweets"""
        try:
            self.count += 1
            text = status.text
            #check wether we got a retweet or not
            logging.debug('count %s found %s - %s' % (self.count, self.found, text))
            if re.match(self.__retweet_pattern, text, re.IGNORECASE) == None:
                return
 
            self.found += 1
 
            if text not in self.retweets.keys():
                twitt_times = 1
            else:
                twitt_times = self.retweets[text] + 1
 
            self.retweets[text] = twitt_times
 
            hour = status.created_at.strftime("%Y%m%d%H")
 
            logging.info("hour: %s - times: %s - %s" % (hour, twitt_times, text))
            logging.info("Number of retweets found:%s" % self.found)
 
            if hour in self.hour_ranking.keys():
                if text in self.hour_ranking[hour].keys():
                    number = self.hour_ranking[hour][text] + 1
                else:
                    number = 1
            else:
                number = 1
                self.hour_ranking[hour] = {}
 
            logging.debug("adding %s to key %s" %(number,text))
            self.hour_ranking[hour][text] = number
            self.printHourlyReport()
 
        except:
            logging.exception("error while analyzing tweets")
 
    def printHourlyReport(self):
        """Print an hourly statistic file in results.txt"""
        logging.debug("updating statistics file")
        with codecs.open("results.txt", "w", "utf-8") as f:
            for h in sorted(self.hour_ranking):
                logging.debug(h + " " + str(type(h)))
                f.write("Top %s tweets at: %s n" % (self.TOP_TWEETS, h))
                count = self.TOP_TWEETS
                h_dict = self.hour_ranking[h]
                #sort retweets by times and then by text
                for t in sorted(h_dict, key=lambda k: (-h_dict[k], k)):
                    line = "%s time%s - %s n" % (h_dict[t],"s" if h_dict[t]>1 else "",t)
                    f.write(line)
                    count -= 1
                    if count == 0:
                        break
                f.write("-------------------------------nn")
 
    def on_error(self, status_code):
        logging.error('An error has occured! Status code = %s' % status_code)
        return True  # keep stream alive
 
    def on_timeout(self):
        logging.info('Time out event')
 
 
def main():
    # Prompt for login credentials and setup stream object
    username = raw_input('Twitter username: ')
    password = getpass('Twitter password: ')
    stream = tweepy.Stream(username, password, TweetListener(), timeout=None)
 
    logging.info("Analyzing Tweeter sample feed. Results.txt will be updated in order to reflect the top 20 retweets of each hour.n")
    stream.sample()
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info('nExecution finished!')
