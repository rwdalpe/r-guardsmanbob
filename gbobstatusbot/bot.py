import time
import signal
import logging
import sys
import config as CFG
from bot_threads import StreamStatusThread, FlairManagerThread


def catch_interrupt_signal(signum, frame):
    logging.info("Caught interrupt. Stopping.")
    sys.exit(0)


logging.basicConfig(filename='gbobstatusbot.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info("Logging into reddit")
config_obj = CFG.get_config_obj()
status_thread = StreamStatusThread(config_obj)
status_thread.start()
flair_thread = FlairManagerThread(config_obj)
flair_thread.start()
signal.signal(signal.SIGINT, catch_interrupt_signal)
# signal.pause() # LINUX ONLY
while(True):
    time.sleep(5.0)