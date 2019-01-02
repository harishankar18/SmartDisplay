from time import time
from os.path import join

""""
    Messages basic type for holding both image and text format of the message
"""


#TODO below classes can also implement equality operator
#TODO Whether template variable can be moved to Messages class as it common to all the classes
#TODO Whether the sequence of the arguments can be changed to avoid passing expiration time.

class Messages(object):
    def __init__(self, content="", expiration_time=86400, timeout=20):
        self.msg_creation_time = time()         #creation time of the message
        self.content = content                  #message content , either it can be text or url
        self.expires_time = expiration_time     #number of days message will be displayed
        self.timeout = timeout        		    #how much time message stays on the screen
        self.refresh_url = "dummy"

    def __str__(self):
        return "Time : " + str(self.msg_creation_time) + " Content =" + str(self.content)

    def __eq__(self, other):
        return self.content == other.content

    def __del__(self):
        pass
