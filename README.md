# Twitch Emote Stats
Welcome to Twitch Emote Stats, a simple Python CLI program that does just that... handle a lot of twitch messages at once and puts them somewhere.  

It can be used to see emote trends depending on certain situations, or whatever you really want. I just made this to get more practice with Python.  
## Installation
```
git clone https://github.com/spliitzx/twitchemotes.git && cd twitchemotes
pip install -r requirements.txt
```

## Running
You need to run the main file first, `twitchemotes.py`, so everything can work.  
```
python3 twitchemotes.py
```

You will then be presented with some options:
```
Welcome to TwitchEmotes!
Twitch Channel: #
```
Enter the desired Twitch channel where you want to analyse emote stats, it will then grab all BetterTTV, FrankerFaceZ, and global twitch emotes (this may take a couple of seconds). After that, it's already listening for emotes.  

To view/play with your data just run or edit `process.py`  
Currently, I've set up a simple way to view the usage data in a graph, which updates every second. You can **run both processes** simultaneously to get live updates, it's cool.  

## Known Bugs
* Communicating between twitchemotes.py and process.py during simultaneous execution is currently using file io via pickle. (because tkinter is a terrible backend) - might fix, works for now

