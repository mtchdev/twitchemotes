import yaml
import json
import urllib.request as request
import sys

class Emote(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url

def get_emotes(ffz_url, bttv_url, channel):
    b_raw = json.loads(request.urlopen(bttv_url + channel).read())
    f_raw = json.loads(request.urlopen(ffz_url + channel).read())
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

    print(f"Loaded {len(emotes)} custom emoticons.")

if __name__ == "__main__":
    print("Welcome to TwitchEmotes!")

    with open("api.yaml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        ffz = data["ffz_url"]
        bttv = data["bttv_url"]

    user = input("Twitch Channel: #")
    get_emotes(ffz, bttv, user)
