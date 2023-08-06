from .import datetime, os
start_time = datetime.now()
from time import sleep
from pyloggerutils import Logger

# def get_logger(**kwargs):
#     return Logger(**kwargs)

class Utilities():

    MODULE = __name__

    def __init__(self, **kwargs):
        if "name" not in kwargs:
            kwargs["name"] = (f"{__class__}".split("'")[1])
        self.get_logger(**kwargs)
        self.debug(f"Initialized: {kwargs['name']}")

    def get_logger(self, **kwargs):
        logger = Logger(**kwargs)
        self.info = logger.info
        self.error = logger.error
        self.warning = logger.warning
        self.debug = logger.debug
        self.critical = logger.critical
        self.logger = logger

    def parent_dir(self, filename):
        expanded_dir = os.path.expanduser(filename)
        realpath_dir = os.path.realpath(expanded_dir)
        directory = os.path.dirname(realpath_dir)
        return directory

    # decode
    # * Decodes a byte to ("UTF-8") String
    # @param message    - Message to be decoded
    # @return String
    def decode(self, message):
        return message.decode("utf-8").strip()
    
    def time_elapsed():
        return datetime.now() - start_time

    def sleep(self, sleep_time=1, message=None):
        if message:
            self.debug(f"Sleeping for {sleep_time}s, Reason: {message}")
        sleep(sleep_time)

    # file_exists
    # * Checks if a file exists in the given path
    # @param file_path  - Path of the file to check
    # @return bool
    def file_exists(self, file_path):
        return os.path.exists(file_path)

    # check_and_create_dir
    # * Checks if the folder exists, if not create a folder in the location
    # @param full_path  - Full path of the folder to be created
    # @return None
    def check_and_create_dir(self, full_path):
        if(not self.file_exists(full_path)):
            os.makedirs(full_path)