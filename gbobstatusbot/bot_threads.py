"""Define threads to perform specific bot tasks"""
import threading
import time
import logging
from flair import update_flair
import stream_status 
import config as CFG


class StreamStatusThread(threading.Thread):
    """Thread that updates a subreddit's sidebar text based on the status of a
    twitch.tv stream"""
    def __init__(self, config):
        """Create a StreamStatusThread based on a configuration dictionary
        
        This thread is daemonic and will automatically initialize a PRAW
        Reddit instance. 
        
        Args:
            config: A dictionary object containing certain configuration
                parameters as described in configuration documentation.
        
        Raises:
            KeyError: Raised when the configuration object does not contain the
                appropriate key-value pairs.
        
        """
        self.reddit = CFG.create_gbobstatusbot_reddit_instance(config)
        toplevel = "StreamStatusBot"
        if(toplevel in config and type(config[toplevel]) is dict):
            config = config[toplevel]
            self.update_interval = CFG.get_update_interval(config)
            self.subreddit = CFG.get_subreddit(config)
            self.stream_name = self.get_stream_name(config)
        else:
            raise KeyError("Couldn't find key %s in config" % toplevel) 
        threading.Thread.__init__(self)
        self.daemon = True
    
    def get_stream_name(self, config):
        """Get the name of the stream this thread monitors
        
        Args:
            config: A dictionary object containing the configuration parameters
                passed to __init__
        
        Returns:
            A string representation of the name of the twitch.tv stream
        
        Raises:
            KeyError: If the configuration options do not contain the
                appropriate key-value pair
        
        """
        stream_name_key = "StreamName"
        if(stream_name_key in config and type(config[stream_name_key]) is str):
            return config[stream_name_key]
        else:
            raise KeyError("Couldn't find key %s in config" % stream_name_key)
    
    def run(self):
        """On a configurable update interval, update a subreddit's sidebar text
        based on stream status and game if appropriate."""
        cur_stream_status = None
        current_game = None
        while(True):
            stream_obj = stream_status.get_stream_details(self.stream_name)
            if(stream_obj != -1):
                new_stream_status = stream_status.is_stream_online(stream_obj)
                logging.debug("Got new stream status: %s" % str(new_stream_status))
                new_game = stream_status.which_game_playing(stream_obj)
                logging.debug("Got new game: %s" % str(new_game))
                if(stream_status.should_update_sidebar(cur_stream_status, 
                                                       new_stream_status, 
                                                       current_game, 
                                                       new_game)):
                    stream_status.update_sidebar(self.reddit, self.subreddit, 
                                                 self.stream_name, 
                                                 new_stream_status, 
                                                 new_game)
                cur_stream_status = new_stream_status
                current_game = new_game
            time.sleep(self.update_interval)


class FlairManagerThread(threading.Thread):
    """Thread that manages a subreddit's link flair"""
    def __init__(self, config):
        """Create a FlairManagerThread based on a configuration dictionary
        
        This thread is daemonic and will automatically initialize a PRAW
        Reddit instance. 
        
        Args:
            config: A dictionary object containing certain configuration
                parameters as described in configuration documentation.
        
        Raises:
            KeyError: Raised when the configuration object does not contain the
                appropriate key-value pairs.
        
        """
        self.reddit = CFG.create_gbobstatusbot_reddit_instance(config)
        toplevel = "FlairBot"
        if(toplevel in config and type(config[toplevel]) is dict):
            config = config[toplevel]
            self.update_interval = CFG.get_update_interval(config)
            self.subreddit = CFG.get_subreddit(config)
            self.mapping = self.get_mapping(config)
        else:
            raise KeyError("Couldn't find key %s in config" % toplevel) 
        threading.Thread.__init__(self)
        self.daemon = True
    
    def get_mapping(self, config):
        """Get a mapping of regexes to link flair CSS class labels
        
        Args:
            config: A dictionary object containing the configuration parameters
                passed to __init__
        
        Returns:
            A dictionary object where the keys are regexes and the values are
            link flair CSS class labels.
        
        Raises:
            KeyError: If the configuration options do not contain the
                appropriate key-value pair
        
        """
        mapping_key = "Mapping"
        if(mapping_key in config and type(config[mapping_key]) is dict):
            return config[mapping_key]
        else:
            raise KeyError("Couldn't find key %s in config" % mapping_key)
    
    def run(self):
        """On a configurable update interval, assign link flair to submissions
        on the subreddit."""
        while(True):
            update_flair(self.reddit, self.subreddit, self.mapping)
            time.sleep(self.update_interval)