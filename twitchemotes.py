import yaml
import json
import urllib.request as request
import sys
import twitch
import time
import pickle
from config import OAUTH

class Emote(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url

class Graph(object):
    usage = {}

    def __init__(self):
        print("created graph")

    def add_usage(self, emote):
        try:
            i = self.usage[emote.name]
            self.usage[emote.name] = i+1
        except KeyError:
            self.usage[emote.name] = 1
            pass

        print(self.usage)

class TwitchStats(object):

    usage = [] # main usage array with types Usage

    def __init__(self, apis, channel):
        # get emotes first
        self.emotes = get_emotes(apis, channel)
        self.channel = "#" + channel
        self.graph = Graph()
        self.monitor()

    def monitor(self):
        print(f"Watching for messages in {self.channel}...")
        twitch.Chat(channel=self.channel, nickname="spliitzx", oauth=OAUTH).subscribe(lambda message: self.handle_message(message))

    def handle_message(self, message):
        msg = message.text
        for emote in self.emotes:
            for x in range(msg.count(emote.name)):
                print(f"Found {emote.name}!")
                self.usage.append({"emote": emote, "time": int(time.time())})
                self.file_out()
                self.graph.add_usage(emote)

    def file_out(self):
        with open("usage.obj", "wb") as f:
            pickle.dump(self.usage, f)

def get_emotes(apis, channel):
    b_raw = json.loads(request.urlopen(apis["bttv_url"] + channel).read())
    f_raw = json.loads(request.urlopen(apis["ffz_url"] + channel).read())
    all_raw = json.loads(request.urlopen(apis["all_url"]).read())
    bg_raw = json.loads(request.urlopen(apis["bttv_global_url"]).read())
    fg_raw = json.loads(request.urlopen(apis["ffz_global_url"]).read())
    ffz = next(iter(f_raw["sets"].values()))["emoticons"]

    emotes = [] # the emotes array

    for emote in b_raw["emotes"]:
        bttv_uri_template = "https:" + b_raw["urlTemplate"]
        url = bttv_uri_template.replace("{{id}}", emote["id"]).replace("{{image}}", "1x")
        x = Emote(emote["code"], url)
        emotes.append(x)

    for emote in ffz:
        url = "https:" + emote["urls"]["1"]
        x = Emote(emote["name"], url)
        emotes.append(x)

    for emote in all_raw:
        x = Emote(emote, None)
        emotes.append(x)

    for emote in bg_raw["emotes"]:
        bttv_uri_template = "https:" + bg_raw["urlTemplate"]
        url = bttv_uri_template.replace("{{id}}", emote["id"]).replace("{{image}}", "1x")
        x = Emote(emote["code"], url)
        emotes.append(x)

    for emote in fg_raw["emoticons"]:
        url = "https:" + emote["urls"]["1"]
        x = Emote(emote["name"], url)
        emotes.append(x)

    print(f"Loaded {len(ffz) + len(b_raw['emotes'])} custom emoticons and found {len(all_raw) + len(bg_raw['emotes']) + len(fg_raw['emoticons'])} default emotes.")
    return emotes

if __name__ == "__main__":
    print("Welcome to TwitchEmotes!")

    with open("api.yaml") as f:
        apis = yaml.load(f, Loader=yaml.FullLoader)

    user = input("Twitch Channel: #")
    TwitchStats(apis, user)

