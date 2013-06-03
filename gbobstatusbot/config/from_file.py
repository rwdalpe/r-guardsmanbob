"""Contain utilities for interfacing with bot configuration file"""
import json
from praw import Reddit
import logging

def get_logfile_name(config):
    """Retrieve the name of the logfile to write, if any"""
    logfile_name_key = "LogFile"
    if(logfile_name_key in config):
        if(type(config[logfile_name_key]) is str):
            return config[logfile_name_key]
        else:
            return None
    else:
        raise KeyError("Couldn't find key %s in config" % logfile_name_key)


def get_logging_level(config):
    """Get the desired level of logging. The default is WARNING if none is
    specified."""
    logging_level_key = "LoggingLevel"
    if(logging_level_key in config):
        if(type(config[logging_level_key]) is str):
            level_str = config[logging_level_key].upper()
            try:
                level = getattr(logging, level_str)
            except AttributeError:
                raise KeyError("%s was not a valid logging level" % logging_level_key)
            else:
                return level
        else:
            return logging.WARNING
    else:
        raise KeyError("Couldn't find key %s in config" % logging_level_key)


def get_config_obj(filename='config.json'):
    """Read a JSON file and return a configuration dictionary"""
    config_obj = None
    with open(filename, 'r') as config:
        config_obj = json.load(config)
    return config_obj


def get_update_interval(config):
    """Retrieve the UpdateInterval parameter from a dictionary object
    
    Args:
        config: A dictionary containing configuration parameters for a bot. For
            this method to be effective, config must contain a UpdateInterval
            parameter.
    
    Returns:
        A floating number representing an update interval in seconds
    
    Raises:
        KeyError: Raised if no UpdateInterval parameter is present in the
            configuration dictionary
    
    """
    updt_intvl_key = "UpdateInterval"
    if(updt_intvl_key in config and type(config[updt_intvl_key]) is float):
        return config[updt_intvl_key]
    else:
        raise KeyError("Couldn't find key %s in config" % updt_intvl_key)


def get_subreddit(config):
    """Retrieve the Subreddit parameter from a dictionary object
    
    Args:
        config: A dictionary containing configuration parameters for a bot. For
            this method to be effective, config must contain a Subreddit
            parameter.
    
    Returns:
        A string representing a subreddit's name
    
    Raises:
        KeyError: Raised if no Subreddit parameter is present in the
            configuration dictionary
    
    """
    sbrdt_key = "Subreddit"
    if(sbrdt_key in config and type(config[sbrdt_key]) is str):
        return config[sbrdt_key]
    else:
        raise KeyError("Couldn't find key %s in config" % sbrdt_key)


def create_gbobstatusbot_reddit_instance(config):
    """Create a new PRAW Reddit object
    
    Args:
        config: A dictionary containing configuration parameters for a bot. This
            configuration dictionary must contain Username, Password, and
            UserAgent keys, as documented in the configuration documentation.
    
    Returns:
        A logged-in PRAW Reddit object instance. None if something does wrong
        but no exception is raised.
    
    Raises:
        KeyError: Raised if any of the required key-value pairs are missing
        from the configuration.
    
    """
    usragnt_key = "UserAgent"
    uname_key = "Username"
    pwd_key = "Password"
    r = None
    if(usragnt_key in config and type(config[usragnt_key]) is str):
        useragent = config[usragnt_key]
        r = Reddit(useragent)
        if(uname_key in config and type(config[uname_key]) is str):
            username = config[uname_key]
            if(pwd_key in config and type(config[pwd_key]) is str):
                password = config[pwd_key]
                r.login(username, password)
            else:
                raise KeyError("Couldn't find key %s in config" % pwd_key)
        else:
            raise KeyError("Couldn't find key %s in config" % uname_key)
    else:
        raise KeyError("Couldn't find key %s in config" % usragnt_key)
    return r