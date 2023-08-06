from main import Downloader
import time

if __name__ == "__main__":
    d = Downloader()
    # url = "https://gamedownloads.rockstargames.com/public/installer/Rockstar-Games-Launcher.exe"
    url = r"https://upcdn.io/kW15bUL/raw/y2mate.com%20-%20How%20to%20make%20dlls%20for%20m%20centers%20Minecraft%20bedrock_1080p.mp4"
    d.headers = {"Authorization": "Bearer public_kW15bUL8oWrFf4ZvEEcU5cGfpMp3"}
    d.start(
        url,
        "r.exe",
        2,
        retries=2,
        display=True,
        multithread=True,
        block=False
    )

    # time.sleep(2)
    # d.stop()
    # time.sleep(5)
    # d.start(url, "r.exe",2,retries=2,block=False)
    # time.sleep(2)
    # d.stop()
    # time.sleep(5)
    # d.start(url, "r.exe",2,retries=2)
    # time.sleep(2)
    # d.start(url, "r.exe",2,retries=2,multithread=False)
    # time.sleep(2)
    # d.stop()
    # time.sleep(2)
    # d.start(url, "r.exe",2,retries=2,block=False)
    # time.sleep(2)
    # d.start(url, "r.exe",2,retries=2,block=False,multithread=False)

# import requests


# head = requests.head(url, timeout=20)

# print(head.headers)

# x = {1: 2, 3: 4}
# print(x)
# y = {1:3}
# x.update(y)
# print(x)
