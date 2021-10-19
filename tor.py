
import os

from stem import Signal
from stem.control import Controller
from dotenv import load_dotenv
load_dotenv()

TOR_KEY = os.getenv('TOR') #Grab key from .env file

class SwitchIP:
    def switch_ip():
        with Controller.from_port(port = 9051) as controller:
            controller.authenticate(password=TOR_KEY) # Password is defined in .env file as TOR_KEY
            controller.signal(Signal.NEWNYM)
            controller.close()