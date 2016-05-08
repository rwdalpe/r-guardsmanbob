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
