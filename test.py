import time
import glob
import pickle
import numpy as np
from utils import RunningStats
from pynput.keyboard import Key, Listener
from statistics import NormalDist
import pyautogui
from threading import Thread


N_GRAM = 3
d = {}
q = []
t = {}

person_name = ""
max_score = 0


def load_template():
    templates = {}
    for filename in glob.glob("template/*.pickle"):
        with open(filename, "rb") as handle:
            templates[filename[9:-7]] = pickle.load(handle)
    return templates


def on_press(key):
    cal(str(key), "p")


def on_release(key):
    if key == Key.esc:
        return False
    cal(str(key), "r")


def _cal_c(m1, m2, std1, std2):
    area = NormalDist(mu=m1, sigma=std1).overlap(NormalDist(mu=m2, sigma=std2))
    return area ** (1 / 4)


def cal(key, event):
    global q, d, person_name, max_score
    _t = time.time()
    if event == "p":
        d[key] = _t
    else:
        if key not in d:
            return
        _time = _t - d[key]
        if key not in t:
            t[key] = RunningStats()
        t[key].update(_time)

    q += [(_t, key + event)]
    if len(q) > N_GRAM:
        q.pop(0)
    for i in range(2, min(len(q), N_GRAM)):
        k = "".join([e[1] for e in q[-i:]])
        _time = q[-1][0] - q[-i][0]
        if key not in t:
            t[key] = RunningStats()
        t[key].update(_time)

    max_score = 0
    for person in templates:
        tem = templates[person]
        prop = []
        count = 0
        for k in t:
            if k in tem:
                m1 = t[k].get_mean()
                m2 = tem[k].get_mean()
                std1 = t[k].get_std()
                std2 = tem[k].get_std()
                if std1 and std2:
                    c = t[k].get_count()
                    count += c
                    prop += [_cal_c(m1, m2, std1, std2) * c]
        # print(person, np.sum(prop) / count, end="\t")
        score = np.sum(prop) / count
        if score > max_score:
            # print(person, score)
            person_name = person
            max_score = score
    # print("")


def get_person_name():
    global person_name
    print("-", person_name)
    return person_name


def start_auth():
    global templates, thread, max_score, person_name
    templates = load_template()
    # person_name = ""
    max_score = 0

    # create a thread
    thread = Thread(target=listen)
    thread.start()


def listen():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def stop_auth():
    global max_score, person_name
    pyautogui.press("esc")
    # person_name = ""
    max_score = 0


thread = None
