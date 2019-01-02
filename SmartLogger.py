import logging

#TODO : Log rotation needs to be implemented

class SmartLogger:
    def __init__(self, cfg):
        self.log_file_name = cfg.parser.get("logging", "log_file_path")
        print "The extracted log file path is ", self.log_file_name
        logging.basicConfig(filename=self.log_file_name, level=logging.DEBUG)
        self.smart_logger = logging.getLogger("smartdisplay")

    def get_smart_logger(self):
        return self.smart_logger


if __name__ == "__main__":
    sm = SmartLogger().get_smart_logger()
    sm.info("Test log is activated")
