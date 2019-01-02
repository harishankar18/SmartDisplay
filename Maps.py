from Messages import Messages
import json
from urllib2 import urlopen
from threading import Thread
from time import sleep


class Maps(Thread):
    def __init__(self, config, message_queue, source="Manyata+Tech+Park,Nagawara"):
        Thread.__init__(self)
        self.cfg = config
        self.API_KEY = config.parser.get('maps', 'API_KEY')
        self.destinations = config.parser.get('source_and_destinations',  'destinations').split(",")
        self.endpoint = config.parser.get('maps', 'REQUEST_PREFIX')
        self.source = source
        self.message_queue = message_queue
        self.interval = 86400

    def prepare_request_url(self, destination):
        req = "units=imperial&origins=" + self.source + "&destinations=" + destination + ",Bangalore&key=" + self.API_KEY
        print "Prepared url is ", self.endpoint + req
        return self.endpoint + req

    def prepare_traffic_data(self):
        traffic_data = "Traffic situation in Bangalore now " + "\n"
        traffic_data += "Travel time from Manyata Tech Park to " + "\n\n\n"

        for destination in self.destinations:
            response = urlopen(self.prepare_request_url(destination)).read()
            data = json.loads(response)
            print "data fetched is ", data
            traffic_data += data['destination_addresses'][0].split(",")[0] + " takes " + data['rows'][0]['elements'][0]['duration']['text']
            traffic_data += "\n"
        return traffic_data

    def run(self):
        while True:
            traffic_data = self.prepare_traffic_data()
            ic = ImageCreator(traffic_data, self.cfg)
            image_path = ic.save_in_image_format()
            ms = Messages(image_path, "img")
            self.message_queue.enqueue(ms)
            sleep(self.interval)
