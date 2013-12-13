import argparse
import time
import signal
import logging
import sys
import traceback
import config as CFG
import threading
import socket
from bot.threads import StreamStatusThread, FlairManagerThread


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
    logfile = CFG.get_logfile_name(config_obj)
    loglevel = CFG.get_logging_level(config_obj)

    if(logfile is None):
        logging.basicConfig(level=loglevel, format='%(asctime)s %(message)s')
    else:
        logging.basicConfig(filename=logfile, level=loglevel, format='%(asctime)s %(message)s')

    logging.info("Logging into reddit")

def startBotThreads(config_obj):
    status_thread = StreamStatusThread(config_obj)
    status_thread.start()
    flair_thread = FlairManagerThread(config_obj)
    flair_thread.start()

def main():
    sys.excepthook = log_uncaught_exceptions
    installThreadExcepthook()
    socket.setdefaulttimeout(20.0)

    args = getCommandArguments()

    config_obj = CFG.get_config_obj(args.config)

    setUpLoggingFromConfig(config_obj)
    startBotThreads(config_obj)

    signal.signal(signal.SIGINT, catch_interrupt_signal)

    while(True):
        time.sleep(5.0)

if __name__ == "__main__":
    main()