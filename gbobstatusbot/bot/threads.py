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

"""Define threads to perform specific bot tasks"""
import logging
import threading

import time

from gbobstatusbot.flair.update import update_flair
from gbobstatusbot.reddit import get_reddit_wrapper

from gbobstatusbot.sidebar import stream


class StreamStatusThread(threading.Thread):
    """Thread that updates a subreddit's sidebar text based on the status of a
    twitch.tv stream"""

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.daemon = True
        self._config = config
        (self._stream_name, self._subreddit_name, self._update_interval) = self._extract_config_details(self._config)

    def run(self):
        logging.debug("Stream Status Thread starting")
        reddit_wrapper = get_reddit_wrapper(self._config)
        stream_obj = None
        while (True):
            new_stream_obj = stream.create_stream_object(self._stream_name)
            if (new_stream_obj != None):
                if (stream_obj != None):
                    if (stream.should_update_sidebar(stream_obj,
                                                     new_stream_obj)):
                        stream.update_sidebar(reddit_wrapper,
                                              self._subreddit_name,
                                              new_stream_obj)
                else:
                    stream.update_sidebar(reddit_wrapper, self._subreddit_name,
                                          new_stream_obj)
                stream_obj = new_stream_obj
            time.sleep(self._update_interval)
        logging.debug("Stream status thread stopping")

    def _extract_config_details(self, config):
        config_details = config.BotThreads.StreamStatusBot()
        stream_name = config_details["StreamName"]
        subreddit_name = config_details["Subreddit"]
        update_interval = config_details["UpdateInterval"]
        return (stream_name, subreddit_name, update_interval)


class FlairManagerThread(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.daemon = True
        self._config = config
        (self._subreddit_name, self._update_interval, self._mapping) = self._extract_config_details(self._config)

    def get_mapping(self, config):
        mapping_key = "Mapping"
        if (mapping_key in config and type(config[mapping_key]) is dict):
            return config[mapping_key]
        else:
            raise KeyError("Couldn't find key %s in config" % mapping_key)

    def run(self):
        logging.debug("Flair management thread starting")
        reddit_wrapper = get_reddit_wrapper(self._config)
        while(True):
            update_flair(reddit_wrapper, self._subreddit_name, self._mapping)
            time.sleep(self._update_interval)
        logging.debug("Flair management thread stopping")

    def _extract_config_details(self, config):
        config_details = config.BotThreads.FlairBot()
        subreddit_name = config_details["Subreddit"]
        update_interval = config_details["UpdateInterval"]
        mapping = config_details["Mapping"]
        return (subreddit_name, update_interval, mapping)

