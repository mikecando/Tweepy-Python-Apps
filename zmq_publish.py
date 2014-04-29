import zmq
import time

ctx = zmq.Context()
s = ctx.socket(zmq.PUB)
s.bind("tcp://*:5567")


while(True):
    s.send("running")
    time.sleep(10)