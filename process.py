import pickle
from twitchemotes import Emote
import time
from collections import OrderedDict
from operator import itemgetter
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
            _sort = OrderedDict(sorted(obj.items(), key=itemgetter(1), reverse=True))
            
            sort = dict(list(_sort.items())[:20])

            y = range(len(sort))
            x = list(sort.values())
            plt.barh(y, x, align="center", color="red")
            plt.yticks(y, list(obj))
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

