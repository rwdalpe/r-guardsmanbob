"""Manage ta subreddit's sidebar and update it with twitch.tv stream status"""
import json
import logging
import urllib
import socket
import http.client


def change_sidebar_text(desc, live):
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


def is_stream_live(stream_name):
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
                return (('stream' in body) and (type(body['stream']) is dict))
        else:
            logging.warning("non 200 status: %d" % twitch.status)
            return -1


def update_sidebar(reddit, sub_name, stream_name, current_stream_status):
    """Update a subreddit's sidebar text.
    
    Args:
        reddit: A PRAW Reddit object for a moderator of the subreddit. This
            object should be authenticated.
        sub_name: A string representation of a subreddit's name
        stream_name: A string representation of a twitch.tv stream's name
        current_stream_status: A boolean value representing if the stream is
            currently known to be online.
    
    """
    logging.info("Updating sidebar for subreddit %s and stream %s" 
                 % (sub_name, stream_name))
    sub = reddit.get_subreddit(sub_name)
    settings = reddit.get_settings(sub_name)
    new_desc = change_sidebar_text(settings['description'], 
                                   current_stream_status)
    logging.debug(new_desc)
    reddit.update_settings(sub, description=new_desc)


def update_sidebar_if_status_change(reddit, sub_name, stream_name, 
                                    old_stream_status):
    """Determine if a stream's status has changed and update a subreddit's 
    sidebar text if so.
    
    Args:
        reddit: A PRAW Reddit object for a moderator of the subreddit. This
            object should be authenticated.
        sub_name: A string representation of a subreddit's name
        stream_name: A string representation of a twitch.tv stream's name
        old_stream_status: A boolean value representing if the stream is
            currently known to be online. None if the status of the stream is
            unknown. An old_stream_status value of None ALWAYS triggers a
            sidebar text update.
    
    Returns:
        A 2-element array of boolean values. The first value is the current
        status of the stream: True if online, False otherwise, None if unknown. 
        The second value is True if the sidebar text was updated, and False 
        otherwise.
    
    """
    cur_stream_status = is_stream_live(stream_name)
    if(cur_stream_status != -1):
        if(old_stream_status is None or old_stream_status != cur_stream_status):
            logging.info("Stream online status changed from %s to %s" 
                         %(str(old_stream_status), str(cur_stream_status)))
            update_sidebar(reddit, sub_name, stream_name, cur_stream_status)
            return [cur_stream_status, True]
    return [old_stream_status, False]