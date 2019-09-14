import pickle
from twitchemotes import Emote
import time
import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

SECONDS_SPLIT = 5

def process_data():
    try:
        with open("usage.obj", "rb") as f:
            x = pickle.load(f)
            last = x[0]["time"]
            batch = [[]]
            iteration = 0
            for i in x:
                time = i["time"]
                seconds = time-last
                if seconds < SECONDS_SPLIT:
                    batch[iteration].append(i["emote"].name)
                else:
                    last = time
                    iteration += 1
                    batch.append([])

            for x in range(len(batch)):
                c = Counter(batch[x]).most_common(5)
                print(f"MOST USED BETWEEN {x*SECONDS_SPLIT} AND {(x+1)*SECONDS_SPLIT} SECONDS:")
                print(c)

    except IOError:
        print("Couldn't find usage.obj, have you run twitchemotes.py yet?")
        sys.exit()

def graph_data():
    try:
        with open("graph.obj", "rb") as f:
            obj = pickle.load(f)

            x = range(len(obj))
            y = list(obj.values())
            plt.barh(x, y, align="center")
            plt.yticks(x, list(obj))
            plt.draw()
            plt.pause(0.001)

    except IOError:
        print("Could'nt find graph.obj, have you run twitchemotes.py yet?")
    except EOFError:
        pass # silent pass

if __name__ == "__main__":
    graph_data()
    plt.show()
    while True:
        graph_data()
        time.sleep(1)

