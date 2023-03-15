import subprocess
import threading
import time

import pymiere


def run_premiere():
    print("thread")
    subprocess.run(
        ["C:\\Program Files\\Adobe\\Adobe Premiere Pro 2023\\Adobe Premiere Pro.exe"]
    )
    # subprocess.run(["cmd", "C:\\Users\\admin\\Documents\\project\\auto-scraping\\default.prproj", "-lha"])


# print(project)


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


x1 = threading.Thread(target=run_premiere)
x2 = threading.Thread(target=main)
x1.start()
x2.start()

x1.join()
x2.join()
