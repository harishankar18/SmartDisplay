from weather import Weather
from Messages import Messages
from time import sleep
from threading import Thread
from flask import render_template


class WeatherMessage(Messages):
    def __init__(self, content, expire_time, timeout, template):
        super(WeatherMessage, self).__init__(content, expire_time, timeout)
        self.template = template

    def render_page(self):
        return  render_template(self.template, page_timeout=self.timeout)

    def __del__(self):
        pass


class WeatherReport(Thread):
    def __init__(self, cfg, message_queue, logger):
        Thread.__init__(self)
        self.weather = Weather()
        self.cfg = cfg
        self.message_queue = message_queue
        self.logger = logger

        self.place          = self.cfg.parser.get('weather', 'location')
        self.template       = self.cfg.parser.get('weather', 'template')
        self.timeout        = self.cfg.parser.getint('weather', 'timeout')
        self.expiration     = self.cfg.parser.getint('weather', 'expiration')

        self.location = self.weather.lookup_by_location(self.place)
        self.forecasts = self.location.forecast()

    def get_today_forecast(self):
        pass

    def predict(self):

        for forecast in self.forecasts:
            print forecast.text()
            print forecast.date()
            print forecast.high()
            print forecast.low()

    def create_weather_report(self):
        message = WeatherMessage("", self.expiration, self.timeout, self.template)
        self.message_queue.enqueue(message)

    def run(self):
        """
        run method monitors weather in indefinite loop
        :return:
        """
        while True:
            self.create_weather_report()
            sleep(self.expiration)

