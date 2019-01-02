from time import time
from itertools import cycle
from NoItemsInQueue import NoItemsInQueue

"""
    Current MessageQueue class stores different
"""
class MessageQueue:
    def __init__(self, logger):
        self.internal_list = list()
        self.queue = cycle(self.internal_list)
        self.logger = logger

    def enqueue(self, message):
        if message in self.internal_list:
            return False
        else:
            self.internal_list.append(message)
            self.queue = cycle(self.internal_list)
        return True

    def dequeue(self):
        """
            When no items are present in the Queue return
            object of NoItemsInQueue.
        """
        if len(self.internal_list) == 0:
            self.logger.info("There are no items in the Queue")
            return NoItemsInQueue()

        item_not_found = True
        message = None
        while item_not_found and len(self.internal_list) > 0:
            current_time = time()
            message = next(self.queue)
            time_difference = (current_time - message.msg_creation_time)
            if  time_difference > message.expires_time:
                log_message =  "Item ", str(message), "is expired length of the queue is ", len(self.internal_list)
                self.logger.info(log_message)
                self.internal_list.remove(message)
                self.queue = cycle(self.internal_list)
            else:
                item_not_found = False
        return message

"""
    Wrapper for handling the multiple queues
    Delete functionality should be added for 
    deleting messages through separate web interface.
"""

class MultiMessageQueue:
    def __init__(self, logger, config):
        """
            There should better way to manager the multilevel queue as
            items always remain common.
            By keeping only the pointers to the latest Queue
        """
        self.multi_queue = {}       #This is the Queue of Queue for storing items for all devices
        self.devices = config.parser.get('Application', 'devices').split(",")
        for device in self.devices:
            self.multi_queue[device] = MessageQueue(logger)


    def enqueue(self, message):
        for local_queue in self.multi_queue.keys():
            self.multi_queue[local_queue].enqueue(message)

    def dequeue(self, client):
        if client in self.multi_queue:
            return self.multi_queue[client].dequeue()
