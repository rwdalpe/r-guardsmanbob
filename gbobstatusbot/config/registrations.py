from gbobstatusbot.bot.broker import BotBroker
from gbobstatusbot.bot.threads import *

def get_bot_broker():
    broker = BotBroker()
    broker.register("StreamStatusBot", lambda config_obj: StreamStatusThread(config_obj))
    broker.register("FlairBot", lambda config_obj: FlairManagerThread(config_obj))
    return broker