"""Manage ta subreddit's sidebar and update it with twitch.tv stream status"""
import json
import logging
import urllib
import socket
import http.client
import re


def change_sidebar_playing(desc, playing):
    """Change sidebar text to reflect the currently played game
    
    Args:
        desc: A string representation of sidebar text
        playing: A string representation of the currently played game
    
    Returns:
        A string representation of sidebar text that properly represents the
        currently played game
    
    """
    match = re.search(r'\[.*\]', playing)
    new_game = match.group(0)
    desc = re.sub(r'\[.*\]', new_game, desc, 1)
    return desc
def change_sidebar_stream_status(desc, live):
    """Change sidebar text with updated stream information
    
    Args:
        desc: A string representation of sidebar text
        live: A boolean value of if a stream is online
    
    Returns:
        A string representation of sidebar text that properly represents the
        current status of a stream
    
    """
    if(live):
        desc = desc.replace("OFFLINE", "ONLINE")
    else:
        desc = desc.replace("ONLINE", "OFFLINE")
    return desc


def get_stream_details(stream_name):
    """Determine if a twitch.tv stream is online.
    
    Args:
        stream_name: A string representing the name of the twitch.tv stream to
            examine
    
    Returns:
        True (1) if the stream is online, False (0) if the stream is offline,
        and -1 if there was an error.
    
    """
    logging.debug("checking if stream %s is live" % stream_name)
    try:
        twitch = urllib.request.urlopen('https://api.twitch.tv/kraken/streams/%s' 
                                        % stream_name)
        response = twitch.read()
    except socket.gaierror:
        logging.warning(("GAIError when accessing twitch API." 
                        "Aborting this try."))
        return -1
    except http.client.IncompleteRead:
        logging.warning(("Unable to finish reading request." 
                        "Aborting this try."))
        return -1
    except urllib.error.URLError:
        logging.warning(("URLError when accessing twitch API." 
                        "Aborting this try."))
        return -1 
    else:
        if(twitch.status == 200):
            jbody = response.decode("UTF-8")
            body = json.loads(jbody)
            if(body != None):
                twitch.close()
                if(('stream' in body) and (type(body['stream']) is dict)):
                    stream = body['stream']
                    if(('channel' in stream) and 
                       (type(stream['channel']) is dict)):
                        return stream['channel']
                else:
                    return None
            logging.warning("problem with stream JSON")
            return -1
        else:
            logging.warning("non 200 status: %d" % twitch.status)
            return -1


def is_stream_online(stream_obj):
    return stream_obj is not None


def which_game_playing(stream_obj):
    return stream_obj['status']


def should_update_sidebar(old_stream_status, new_stream_status, old_game, 
                          new_game):
    return ((old_stream_status is None or old_game is None) or 
            old_stream_status != new_stream_status or 
            old_game != new_game)


def update_sidebar(reddit, sub_name, stream_name, current_stream_status, 
                   current_game):
    """Update a subreddit's sidebar text.
    
    Args:
        reddit: A PRAW Reddit object for a moderator of the subreddit. This
            object should be authenticated.
        sub_name: A string representation of a subreddit's name
        stream_name: A string representation of a twitch.tv stream's name
        current_stream_status: A boolean value representing if the stream is
            currently known to be online.
        current_game: A string representation of the game currently being played
    
    """
    logging.info("Updating sidebar for subreddit %s and stream %s" 
                 % (sub_name, stream_name))
    sub = reddit.get_subreddit(sub_name)
    settings = reddit.get_settings(sub_name)
    new_desc = change_sidebar_stream_status(settings['description'], 
                                   current_stream_status)
    new_desc = change_sidebar_playing(new_desc, current_game)
    logging.debug(new_desc)
    reddit.update_settings(sub, description=new_desc)