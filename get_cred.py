import configparser


class HostConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('cred.ini')

    @property
    def TelegramBot(self):
        return self.config["TelegramBot"]

    @property
    def Database(self):
        return self.config["Database"]

    @property
    def UserPhoto(self):
        return self.config["UserPhoto"]

    @property
    def LocationPhoto(self):
        return self.config["LocationPhoto"]


