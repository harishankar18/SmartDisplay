from ConfigParser import SafeConfigParser
from glob import glob

"""
    Reads all the config parameters related to 
    smart tv application
"""


class ConfigReader:
    def __init__(self, config_file_path="Resources"):
        self.files = glob(config_file_path + "/*conf")
        self.parser = SafeConfigParser()

    def read_config(self):
        self.parser.read(self.files)


if __name__ == "__main__":
    cr = ConfigReader()
    cr.read_config()
