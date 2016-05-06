"""Define threads to perform specific bot tasks"""
import logging
import threading

from reddit import get_reddit_wrapper


class StreamStatusThread(threading.Thread):
    """Thread that updates a subreddit's sidebar text based on the status of a
    twitch.tv stream"""

    def __init__(self, config):
        # self.reddit = CFG.create_gbobstatusbot_reddit_instance(config)
        # toplevel = "StreamStatusBot"
        # if(toplevel in config and type(config[toplevel]) is dict):
        #     config = config[toplevel]
        #     self.update_interval = CFG.get_update_interval(config)
        #     self.subreddit = CFG.get_subreddit(config)
        #     self.stream_name = self.get_stream_name(config)
        # else:
        #     raise KeyError("Couldn't find key %s in config" % toplevel)
        threading.Thread.__init__(self)
        self.daemon = True
        self.config = config

    def get_stream_name(self, config):
        stream_name_key = "StreamName"
        if (stream_name_key in config and type(config[stream_name_key]) is str):
            return config[stream_name_key]
        else:
            raise KeyError("Couldn't find key %s in config" % stream_name_key)

    def run(self):
        logging.debug("Stream Status Thread starting")
        reddit_wrapper = get_reddit_wrapper(self.config)
        print(reddit_wrapper.get_username())
        # stream_obj = None
        # while(True):
        #     new_stream_obj = stream.create_stream_object(self.stream_name)
        #     if(new_stream_obj != None):
        #         if(stream_obj != None):
        #             if(stream.should_update_sidebar(stream_obj,
        #                                             new_stream_obj)):
        #                 stream.update_sidebar(self.reddit,
        #                                       self.subreddit,
        #                                       new_stream_obj)
        #         else:
        #             stream.update_sidebar(self.reddit, self.subreddit,
        #                                   new_stream_obj)
        #         stream_obj = new_stream_obj
        #     time.sleep(self.update_interval)
        logging.debug("Stream status thread stopping")


class FlairManagerThread(threading.Thread):
    def __init__(self, config):
        # self.reddit = CFG.create_gbobstatusbot_reddit_instance(config)
        # toplevel = "FlairBot"
        # if(toplevel in config and type(config[toplevel]) is dict):
        #     config = config[toplevel]
        #     self.update_interval = CFG.get_update_interval(config)
        #     self.subreddit = CFG.get_subreddit(config)
        #     self.mapping = self.get_mapping(config)
        # else:
        #     raise KeyError("Couldn't find key %s in config" % toplevel)
        threading.Thread.__init__(self)
        self.daemon = True
        self.config = config

    def get_mapping(self, config):
        mapping_key = "Mapping"
        if (mapping_key in config and type(config[mapping_key]) is dict):
            return config[mapping_key]
        else:
            raise KeyError("Couldn't find key %s in config" % mapping_key)

    def run(self):
        logging.debug("Flair management thread starting")
        reddit_wrapper = get_reddit_wrapper(self.config)
        print(reddit_wrapper.get_username())
        # while(True):
        #     update_flair(self.reddit, self.subreddit, self.mapping)
        #     time.sleep(self.update_interval)
        logging.debug("Flair management thread stopping")
