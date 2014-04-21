#script finds people you follow, and people they follow, etc. up to some depth
#and then finds people who are popular (followed a lot), but who you don't
#follow

import tweepy
import pickle
import re
import tweepy, time, sys
import ConfigParser
import random
import logging
import os

logging.basicConfig(filename='twitter_recommend.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%d %b %Y %H:%M:%S.%p')

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

START_USER= "TGC" #twitter username of person to start exploration on
BLACKLIST= [] #people who shouldn't be expanded
FRIENDS_LIMIT= 20 #how many friends at most do we extract from one person
WAIT_TIME= 0 #in seconds, between each person
MAX_DEPTH= 2 #max depth to consider. User is depth 0
USEPICKLE= False#use pickle to save results, so that we can start script later
                #and begin from where we left off?

try:
    #let's see if we can find work in progress
    ff= open('twitternetwork', 'r')
    network, graph, counts, color= pickle.load(ff)
    ff.close()
    print 'Found a database! Continuing our work....'
except:
    network=[(START_USER, 0)] #tuples of person, depth
    graph=[] #lets just store all edges of this graph
    counts={} #number of times we see a user come up, ever
    color={} #color of every person. 1= currently in Q. 2=explored
    print 'Ok lets do this, from scratch'

i=0
failed=[]
while len(network)>0:
    i=i+1

    #pop a person
    user, depth= network.pop(0)
    color[user]= 2 #mark user as explored

    #only want to go up to depth 2. Don't explore these people anymore
    if depth>=MAX_DEPTH or user in BLACKLIST:
        continue

    limits= api.rate_limit_status()
    #R= limits['remaining_hits']
    R = limits
    print "remaining hits: ", R
    while R<=3:
        time.sleep(10)
        limits= api.rate_limit_status()
        #R= limits['remaining_hits']
        R = limits
        print "Waiting to get more API calls...", time.localtime()

    try:
        #get all friends, but only those with friend counts <200. The other people are weird
        friends=[friend.screen_name for friend in tweepy.Cursor(api.friends, id=user).items(FRIENDS_LIMIT)]
    except:
        print "some error happened when we tried to process this person.", time.localtime()

        #crap what do we do now? Let's put this person to the end and deal with them later?

        #forget them
        friends=[]
        print 'Forgetting about user ' + user + '. API call failed.'
        failed.append(user)

        #just in case there is something wrong with the actual person for some reason
        #color[user]= 1 #put back into Q
        #network.append((user,depth))
        #print "ok put that user, " + user + " to the end, to be dealt with later"

    graph.extend([(user, f) for f in friends])
    novel= [f for f in friends if not f in color] #those that are not yet colored are novel people

    #keep track of everyone we see, and how many times
    for f in friends:
        counts[f]= counts.get(f,0)+1

    print "explored "+user+" at depth "+`depth`+" --Q size: "+`len(network)`+" novel: "+`len(novel)`+"/"+`len(friends)`

    network.extend([(n, depth+1) for n in novel])
    for p in novel:
        color[p]= 1 #currently in Q

    if i%10==0 and USEPICKLE:
        #make backups
        ff= open('twitternetwork', 'w')
        pickle.dump([network, graph, counts, color], ff)
        ff.close()

    if i%10==0:
        #show progress
        blah= [(b,a) for a,b in counts.items()]
        blah.sort()
        print blah

    if WAIT_TIME>0: time.sleep(WAIT_TIME)

if USEPICKLE:
    #save everything
    ff= open('twitternetwork', 'w')
    pickle.dump([network, graph, counts, color], ff)
    ff.close()

#give the recommendations
mine= [v for (u,v) in graph if u==START_USER]
recomm= []
for p in counts:
    if not p in mine:
        recomm.append((counts[p], p))
recomm.sort()
for (v, p) in recomm:
    print "You're not following " + p + " but other " + `v` + " people are!"
    api.create_friendship(p)

print '----'
print 'The following people were not processed because of error:'
for x in failed:
    print x
print 'ALL DONE! Also saved pickle for later'
