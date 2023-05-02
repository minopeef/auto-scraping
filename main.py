#!./.venv/bin/python
import time

from automation.I6496 import I6496
from automation.Livejupiter2 import Livejupiter2
from automation.Nanjstu import Nanjstu
from automation.Rock import Rock
from automation.Yakiusoku import Yakiusoku
from store import Store

classes = ["Rock", "Yakiusoku", "Livejupiter2", "Nanjstu", "I6496"]


def all_run(duration: str):
    while True:
        start_time = time.time()
        for item in classes:
            if Store.flag:
                getattr(globals()[item](), "run")()
            else:
                return
        end_time = time.time()
        remaining_time = int(duration) * 60 - end_time + start_time
        if remaining_time > 1:
            time.sleep(remaining_time)


def manual_run(url: str):
    getattr(globals()[url](), "run")()
