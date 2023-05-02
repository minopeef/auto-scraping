#!./.venv/bin/python
import threading
import time


from automation.I6496 import I6496
from automation.Livejupiter2 import Livejupiter2
from automation.Nanjstu import Nanjstu
from automation.Rock import Rock
from automation.Yakiusoku import Yakiusoku
from app import Store


def all_run(duration):
    while True:
        start_time = time.time()
        if Store.flag:
            # Rock().run()
            # Yakiusoku().run()
            # Livejupiter2().run()
            # Nanjstu().run()
            # I6496().run()
            print(duration)
        end_time = time.time()
        time.sleep(duration - end_time + start_time)
