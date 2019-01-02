from flask import Flask
from MessageQueue import MultiMessageQueue
from ConfigReader import ConfigReader
from Yammer import YammerHandle
from SmartLogger import SmartLogger
from WeatherReport import WeatherReport
from UploadHandler import UploadHandler

class FPDisplay:
    """
        Main class for FPDisplay application which is
        responsible for following tasks.
            1. Reading all the configuration.
            2. starting the monitoring threads.
    """
    def __init__(self, config_directory_path = "Resources/config"):
        self.app = Flask(__name__)

        self.cfg = ConfigReader(config_directory_path)
        self.cfg.read_config()

        self.logger = SmartLogger(self.cfg).get_smart_logger()
        self.message_queue = MultiMessageQueue(self.logger, self.cfg)
        self.upload_handler = UploadHandler(self.app, self.cfg, self.message_queue)

        self.yammer = YammerHandle(self.cfg,  self.message_queue, self.logger)
        #self.weather_report = WeatherReport (self.cfg, self.message_queue, self.logger)

    def handle_request(self):
        @self.app.route('/<device>')
        def fp_display(device):
            print("Received request for the device", device)
            message = self.message_queue.dequeue(device)
            if message is not None:
                return message.render_page(device)
            else:
                return "<h1> Dummy return </h1>"

        @self.app.route('/upload')
        def upload_file():
            return self.upload_handler.render_upload_template()

        @self.app.route('/uploader', methods=['GET', 'POST'])
        def save_file():
            return self.upload_handler.save_file()

    def start(self):
        self.app.run(host='0.0.0.0', port=5000, threaded=True)

    def start_monitoring_threads(self):
        self.yammer.start()
        #self.weather_report.start()


if __name__ == "__main__":
    fd = FPDisplay()
    fd.handle_request()
    fd.start_monitoring_threads()
    fd.start()
