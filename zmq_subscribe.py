import zmq
import subprocess



ctx = zmq.Context()
s = ctx.socket(zmq.SUB)
s.connect("tcp://127.0.0.1:5567")
s.setsockopt(zmq.SUBSCRIBE,'')
poller = zmq.Poller()
poller.register(s, zmq.POLLIN) # POLLIN for recv, POLLOUT for send
print 'waiting...'
#msg = s.recv()
evts = poller.poll(30000) # wait *up to* one second for a message to arrive.
if(len(evts) < 1):
    print 'Process is down and now restarting'
    subprocess.call('pwd')
    #subprocess.call('python tweet_bible_verse.py')
    retcode = subprocess.call(["python tweet_bible_verse.py &"], shell=True)
    print str(retcode)
else:
    print 'Process is running'

