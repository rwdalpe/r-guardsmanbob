import time
import signal
import logging
import sys
import config as CFG
from bot_threads import StreamStatusThread, FlairManagerThread


def catch_interrupt_signal(signum, frame):
    logging.info("Caught interrupt. Stopping.")
    sys.exit(0)


config_obj = CFG.get_config_obj()
logfile = CFG.get_logfile_name(config_obj)
if(logfile is None):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
else:
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info("Logging into reddit")
status_thread = StreamStatusThread(config_obj)
status_thread.start()
flair_thread = FlairManagerThread(config_obj)
flair_thread.start()
signal.signal(signal.SIGINT, catch_interrupt_signal)
# signal.pause() # LINUX ONLY
while(True):
    time.sleep(5.0)