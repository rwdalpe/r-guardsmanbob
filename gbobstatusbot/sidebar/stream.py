# Copyright (c) 2013 Robert Winslow Dalpe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Utilities for dealing with twitch.tv streams and the sidebar"""
import logging
import json
import re
import http.client
import urllib
import socket
import requests
import time


class Stream:
    """Encapsulation object that stores a stream's name, if it's online, and
    the name of the game currently being played."""

    def __init__(self, stream_name, stream_status=None, cur_playing=None):
        """Create a new Stream object
        
        Args:
            stream_name: a string representation of a twitch.tv stream's name
            stream_status: a boolean variable indicating if the stream is
                currently online. None if no data is known about the stream's
                status
            cur_playing: a string representation of the name of the game 
                currently being played on the stream. None if no data is known
                about the currently played game
        
        """
        self.stream_name = stream_name
        self.stream_status = stream_status
        self.cur_playing = cur_playing


def create_stream_object(stream_name):
    """Create a new Stream object
    
    Creates a new Stream object from only the name of the stream by fetching
    raw data from the twitch.tv API.
    
    Args:
        stream_name: the name of the stream to create an object for
    
    Returns:
        A new Stream object or None if there was a problem creating the Stream
        object.
    
    """
    stream_obj = None
    raw_stream_obj = get_raw_stream_obj(stream_name)
    if (raw_stream_obj != None):
        stream_obj = Stream(stream_name)
        logging.debug("Retrieved body of raw stream obj")
        if (('stream' in raw_stream_obj) and
                (type(raw_stream_obj['stream']) is dict)):
            stream = raw_stream_obj['stream']
            if (('channel' in stream) and (type(stream['channel']) is dict)):
                stream_obj.stream_status = True
                cur_playing = get_cur_game(stream['channel'])
                stream_obj.cur_playing = cur_playing if (
                    cur_playing is not None and cur_playing != "[]") else get_cur_game_fallback(stream)

        else:
            stream_obj.stream_status = False
            stream_obj.cur_playing = "[]"
    else:
        logging.warning("problem with raw stream JSON")
    return stream_obj


def get_raw_stream_obj(stream_name):
    """Retrieve the raw JSON data for a twitch.tv stream by querying the 
    twitch.tv API."""
    logging.debug("fetching raw stream obj for stream %s" % stream_name)
    raw_stream_obj = None
    try:
        twitch = urllib.request.urlopen('https://api.twitch.tv/kraken/streams/%s'
                                        % stream_name, timeout=20)
        response = twitch.read()
    except socket.gaierror:
        logging.warning(("GAIError when accessing twitch API. "
                         "Aborting this try."))
    except http.client.IncompleteRead:
        logging.warning(("Unable to finish reading request. "
                         "Aborting this try."))
    except urllib.error.URLError:
        logging.warning(("URLError when accessing twitch API. "
                         "Aborting this try."))
    except urllib.error.HTTPError:
        logging.warning(("HTTPError when accessing twitch API. "
                         "Aborting this try."))
    else:
        if (twitch.status == 200):
            logging.debug("200 OK")
            jbody = response.decode("UTF-8")
            body = json.loads(jbody)
            raw_stream_obj = body
        else:
            logging.warning("non 200 status: %d" % twitch.status)
    finally:
        return raw_stream_obj


def get_cur_game(channel_dict):
    """Find the currently played game from the title of a stream.
    
    This searches for characters contained in square brackets [] and considers
    those to be the title of the currently played game (as well as other
    relevant information). If no match is found, None is
    returned.
    
    """
    if (channel_dict is not None):
        if ('status' in channel_dict and type(channel_dict['status']) is str):
            match = re.search(r'\[.*\]', channel_dict['status'])
            new_game = match.group(0) if (match != None) else None
            return new_game
    return None


def get_cur_game_fallback(stream_dict):
    """Find the currently played game from the JSON of a stream.
    
    In the event that details of the currently played game cannot be found in
    the title of the stream, this is a fallback method that tries to read the
    'game' property of the stream JSON object to determine what game is being
    played. If this yields no results, empty brackets [] are returned.
    
    """
    if ('game' in stream_dict and type(stream_dict['game']) is str):
        return ''.join(('[', stream_dict['game'], ']'))
    else:
        return "[]"


def change_sidebar_playing_text(desc, playing):
    """Change sidebar text to reflect the currently played game
    
    Args:
        desc: A string representation of sidebar text
        playing: A string representation of the currently played game
    
    Returns:
        A string representation of sidebar text that properly represents the
        currently played game
    
    """
    desc = re.sub(r'\[.*\]', playing, desc, 1)
    return desc


def change_sidebar_status_text(desc, is_online):
    """Change sidebar text with updated stream information
    
    Args:
        desc: A string representation of sidebar text
        is_online: A boolean value of if a stream is online
    
    Returns:
        A string representation of sidebar text that properly represents the
        current status of a stream
    
    """
    if (is_online):
        desc = desc.replace("OFFLINE", "ONLINE")
    else:
        desc = desc.replace("ONLINE", "OFFLINE")
    return desc


def should_update_sidebar(old_stream_obj, new_stream_obj):
    """Determine if stream data has changed sufficiently to trigger a sidebar
    text update."""
    old_stream_status = old_stream_obj.stream_status
    old_game = old_stream_obj.cur_playing
    new_stream_status = new_stream_obj.stream_status
    new_game = new_stream_obj.cur_playing
    return ((old_stream_status is None or old_game is None) or
            old_stream_status != new_stream_status or
            old_game != new_game)


def update_sidebar(reddit, sub_name, stream_obj):
    stream_name = stream_obj.stream_name
    current_stream_status = stream_obj.stream_status
    current_game = stream_obj.cur_playing
    logging.info("Updating sidebar for subreddit %s and stream %s"
                 % (sub_name, stream_name))
    try:
        sub = reddit.get_subreddit(sub_name)
        settings = reddit.get_settings(sub_name)
        new_desc = change_sidebar_status_text(settings['description'],
                                              current_stream_status)
        new_desc = change_sidebar_playing_text(new_desc, current_game)
        reddit.edit_wiki_page(sub, "config/sidebar", new_desc)
    except (requests.exceptions.HTTPError):
        logging.warning("HTTPError updating reddit. Waiting 2 seconds and trying again.")
        time.sleep(2.0)
        update_sidebar(reddit, sub_name, stream_obj)
