from aiogram import Router
from abc import ABC, abstractmethod


class AbstractRouter(ABC):
    def __init__(self, session):
        self.router = Router()
        self.session = session
        self.initialize_commands()

    @abstractmethod
    def initialize_commands(self):
        pass

    def get_instance(self):
        return self.router