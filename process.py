import pickle
from twitchemotes import Emote
import time
import sys

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

            print(batch)
    except IOError:
        print("Couldn't find usage.obj, have you run twitchemotes.py yet?")
        sys.exit()

if __name__ == "__main__":
    process_data()

