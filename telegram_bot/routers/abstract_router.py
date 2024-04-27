from aiogram import Router
from abc import ABC, abstractmethod

from telegram_bot.ServiceLocator import ServiceLocator


class AbstractRouter(ABC):
    def __init__(self):
        self.router = Router()
        self.session = ServiceLocator.get_service("session")
        self.initialize_commands()

    @abstractmethod
    def initialize_commands(self):
        pass

    def get_instance(self):
        return self.router