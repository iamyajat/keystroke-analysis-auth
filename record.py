import time
import pandas as pd
from pynput.keyboard import Key, Listener

from time import sleep
from threading import Thread

import pyautogui


df = pd.DataFrame(columns=["time", "key", "event"])


def on_press(key):
    global df
    key = str(key)
    print(key)
    df = pd.concat(
        [df, pd.DataFrame([{"time": time.time(), "key": key, "event": "p"}])]
    )


def on_release(key):
    global df
    df = pd.concat(
        [df, pd.DataFrame([{"time": time.time(), "key": key, "event": "r"}])]
    )
    if key == Key.esc:
        return False


def start_record():
    global df, thread

    # create a thread
    thread = Thread(target=listen)
    thread.start()

    df = pd.DataFrame(columns=["time", "key", "event"])


def stop_record(username):
    global df, thread
    df.to_csv(f"data/{username}.csv", index=False)
    print(df)

    pyautogui.press("esc")

    # thread.join()
    # stop the thrad


def listen():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


thread = None
