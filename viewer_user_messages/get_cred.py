import configparser

CRED_FILE = "D:\diplom\cred.ini"


class HostConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        status = self.config.read(CRED_FILE)
        if not status:
            raise Exception("No credentials in directory diplom\cred.ini")

    @property
    def Database(self):
        return self.config["Database"]

    @property
    def UserPhoto(self):
        return self.config["UserPhoto"]

    @property
    def LocationPhoto(self):
        return self.config["LocationPhoto"]