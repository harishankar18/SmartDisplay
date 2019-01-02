from yampy import Yammer
from Messages import Messages
from datetime import datetime
from threading import Thread
from dateutil.parser import parse
from flask import render_template


#TODO use special formula to count number of letters in the text based on set the timeout value
class YammerMessage(Messages):
    def __init__(self, content, author, expire_time, template, timeout):
        super(YammerMessage, self).__init__(content, expire_time, timeout)
        self.template = template
        self.author = author

    def render_page(self):
        return render_template(self.template, yammer_content=self.content, author_content=self.author, page_timeout=self.timeout)


class YammerHandle(Thread):
    def __init__(self, cfg, message_queue, logger):
        Thread.__init__(self)

        self.cfg = cfg
        self.access_token = self.cfg.parser.get('yammer', 'access_token')
        self.group_id = self.cfg.parser.getint('yammer', 'group_id')
        self.expire_time = self.cfg.parser.getint('yammer', 'message_expire_time')
        self.template = self.cfg.parser.get('yammer', 'template')
        self.timeout = self.cfg.parser.get('yammer', 'timeout')
        self.user_ids = self.cfg.parser.items('yammer_users')

        self.yammer = Yammer(access_token=self.access_token)
        self.message_queue = message_queue
        self.logger = logger

    def validate(self, message, current_date):
        message_timestamp = parse(message['created_at'].split()[0])
        if message_timestamp == current_date and message['group_created_id'] == self.group_id:
            if message['replied_to_id'] is None and message['system_message'] is False:
                return True
        return False

    def write_message(self, message):
        for key in message:
            log_message = str(key) + "=====>" + str(message[key])
            self.logger.info(log_message)

    def parse_message(self, message):
        content = message['body']['rich']
        return content

    def parse_and_validate(self, current_message, current_date):

        if self.validate(current_message, current_date):
                return self.parse_message(current_message)
        return None

    def insert_to_message_queue(self, data, user, current_date):
        log_message = "Receiving messages from user ", user
        self.logger.info(log_message)

        for current_message in data['messages']:
            content = self.parse_and_validate(current_message, current_date)
            if content:
                mq = self.create_msg(content, user)
                self.message_queue.enqueue(mq)

    def create_msg(self, content, user):
        author = str(user).replace("_", " ").title()
        expires_time = self.expire_time
        if "Recruitment" in content:
            expires_time = expires_time * 10
        mq = YammerMessage(content, author, expires_time, self.template, self.timeout)
        return mq

    def run(self):
        while True:
            current_date = datetime.now().isoformat().split('T')[0]
            for user, user_id in self.user_ids:
                #TODO check yampy2 package for retriving messages from specific group
                try:
                    data = self.yammer.messages.from_user(int(user_id), threaded=True)
                    self.insert_to_message_queue(data, user, parse(current_date))
                except:
                    logger_message = "Error occurred while fetching details for ", user
                    self.logger.info(logger_message)
