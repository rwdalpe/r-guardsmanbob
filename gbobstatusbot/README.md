gbobstatusbot
=============

gbobstatusbot is a simple reddit bot that automates some administrative tasks
for [/r/guardsmanbob](http://reddit.com/r/guardsmanbob). It is written in Python
and utilizes the [PRAW](https://praw.readthedocs.org/en/latest/) API wrapper to
interface with the reddit API. The bot is Python 3 compatible.

Responsibilities
----------------

gbobstatusbot is responsible for:

* updating the sidebar of the subreddit with text to indicate whether or not
[GuardsmanBob's twitch.tv stream](http://twitch.tv/guardsmanbob) is online.
* assigning link flair CSS classes to posts.

Configuration
-------------

The bot is configured with a JSON configuration file. A 
[sample configuration](https://github.com/rwdalpe/r-guardsmanbob/blob/master/gbobstatusbot/sampleconfig.json)
file is included in this repository, lacking all specific information for
logging in as the bot, obviously. The bot currently runs two threads (one for
each responsibility, and there are separate configuration sections for each 
thread. The configuration should be fairly self-evident from looking at the
file, but here are the details.

### Top-level configuration options
* **UserAgent**: The user-agent string for the bot, as required by the reddit API
* **Username**
* **Password**

####StreamStatusBot
This is a dictionary containing configuration specific to the thread which
monitors the twitch stream.

* **StreamName**: the name of the stream to monitor (in this case,
"guardsmanbob")
* **Subreddit**: the name of the subreddit to update (in this case,
"guardsmanbob")
* **UpdateInterval**: The number of seconds between polling twitch for stream
status (**SHOULD NOT BE LOWER THAN 10s**)

####FlairBot
This is a dictionary containing configuration specific to the thread which
manages link flair.

* **Subreddit**: the name of the subreddit to update (in this case,
"guardsmanbob")
* **Mapping**: a dictionary where each key is a regex to match against
submission titles, and the value is a CSS class to apply to the submission if
there is a match. Only the first match gets applied.
* **UpdateInterval**: The number of seconds between polling twitch for stream
status (**SHOULD NOT BE LOWER THAN 10s**)

Usage
-----

The bot can be used by running 

`python bot.py`