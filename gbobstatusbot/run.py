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

import argparse
import time
import signal
import logging
import sys
import traceback
import config as CFG
import threading
import socket
from gbobstatusbot.config.registrations import get_bot_broker


def catch_interrupt_signal(signum, frame):
    logging.info("Caught interrupt. Stopping.")
    sys.exit(0)


def installThreadExcepthook():
    """Thread excepthook workaround from http://bugs.python.org/issue1230540#msg91244
    
    Workaround for sys.excepthook thread bug
    From
    http://spyced.blogspot.com/2007/06/workaround-for-sysexcepthook-bug.html
   
    (https://sourceforge.net/tracker/?func=detail&atid=105470&aid=1230540&group_id=5470).
    Call once from __main__ before creating any threads.
    If using psyco, call psyco.cannotcompile(threading.Thread.run)
    since this replaces a new-style class method.
    
    """
    init_old = threading.Thread.__init__

    def init(self, *args, **kwargs):
        init_old(self, *args, **kwargs)
        run_old = self.run

        def run_with_except_hook(*args, **kw):
            try:
                run_old(*args, **kw)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                sys.excepthook(*sys.exc_info())

        self.run = run_with_except_hook

    threading.Thread.__init__ = init


def log_uncaught_exceptions(ex_type, ex, tb):
    logging.critical(''.join(traceback.format_tb(tb)))
    logging.critical('{0}: {1}'.format(ex_type, ex))


def getCommandArguments():
    parser = argparse.ArgumentParser('Run the r-guardsmanbob moderation bot')
    parser.add_argument('-c', '--config', dest='config', type=str,
                        default='config.json', help='a path to the configuration file for the bot to use')
    args = parser.parse_args()
    return args


def setUpLoggingFromConfig(config_obj):
    logfile = config_obj.LogFile()
    loglevel = CFG.get_logging_loglevel(config_obj)

    if (logfile is None):
        logging.basicConfig(level=loglevel, format='%(asctime)s %(message)s')
    else:
        logging.basicConfig(filename=logfile, level=loglevel, format='%(asctime)s %(message)s')


def get_bot_threads(config_obj, bot_broker):
    bot_threads = []
    for bot_thread_key, bot_thread_value in config_obj.BotThreads:
        bot_threads.append(bot_broker.broker(bot_thread_key, config_obj))
    return bot_threads


def main():
    sys.excepthook = log_uncaught_exceptions
    installThreadExcepthook()
    socket.setdefaulttimeout(20.0)

    args = getCommandArguments()

    config_obj = CFG.get_config_obj(args.config)

    setUpLoggingFromConfig(config_obj)

    bot_broker = get_bot_broker()

    bot_threads = get_bot_threads(config_obj, bot_broker)

    for bot_thread in bot_threads:
        bot_thread.start()

    signal.signal(signal.SIGINT, catch_interrupt_signal)

    while (True):
        time.sleep(5.0)


if __name__ == "__main__":
    main()
