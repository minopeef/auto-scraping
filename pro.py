import os
import threading
import time

import pymiere


# stdout
def run_premiere():
    print("thread")
    os.popen("default.prproj")


def main():
    while True:
        try:
            print(pymiere.objects.app.isDocumentOpen())
            project = pymiere.objects.app.project
            print(project)
            print("hello world")
            break
        except:  # noqa
            time.sleep(3)
    print("opened")
    print(2)


x1 = threading.Thread(target=run_premiere)
x2 = threading.Thread(target=main)
x1.start()
x2.start()

x1.join()
x2.join()
