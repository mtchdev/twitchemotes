import pickle
from twitchemotes import Emote

with open("usage.obj", "rb") as f:
    x = pickle.load(f)
    for i in x:
        #print(i["emote"].name)
        print(f"{i['time']} for {i['emote'].name}")

