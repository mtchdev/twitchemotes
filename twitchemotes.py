import yaml
import json
import urllib.request as request
import sys
import twitch
import time
from config import OAUTH

class Emote(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url

class TwitchStats(object):

    usage = [] # main usage array with types Usage

    def __init__(self, urlset, channel):
        # get emotes first
        self.emotes = get_emotes(urlset[0], urlset[1], urlset[2], channel)
        self.channel = "#" + channel
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

def get_emotes(ffz_url, bttv_url, all_url, channel):
    b_raw = json.loads(request.urlopen(bttv_url + channel).read())
    f_raw = json.loads(request.urlopen(ffz_url + channel).read())
    all_raw = json.loads(request.urlopen(all_url).read())
    bttv = b_raw["emotes"]
    ffz = next(iter(f_raw["sets"].values()))["emoticons"]
    if not bttv or not ffz:
        print("No emoticon sets found.")
        sys.exit()

    emotes = []

    for emote in bttv:
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

    print(f"Loaded {len(ffz) + len(bttv)} custom emoticons and found {len(all_raw)} default emotes.")
    return emotes

if __name__ == "__main__":
    print("Welcome to TwitchEmotes!")

    with open("api.yaml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        ffz = data["ffz_url"]
        bttv = data["bttv_url"]
        all_ = data["all_url"]

    user = input("Twitch Channel: #")

    urlset = [
            ffz,
            bttv,
            all_
        ]
    TwitchStats(urlset, user)

