"""Contain utilities for interfacing with bot configuration file"""
import logging

import jsoncfg


def get_logging_loglevel(config):
    """Get the desired level of logging. The default is WARNING if none is
    specified."""
    if (jsoncfg.node_exists(config.LoggingLevel)):
        try:
            level = getattr(logging, config.LoggingLevel())
        except AttributeError:
            raise KeyError("%s was not a valid logging level" % config.LoggingLevel)
        else:
            return level
    else:
        return logging.WARNING


def get_config_obj(filename='config.json'):
    """Read a JSON file and return a configuration dictionary"""
    config_obj = jsoncfg.load_config(filename)
    return config_obj
