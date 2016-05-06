class BotBroker:
    def __init__(self):
        self.broker_dict = {}
    def register(self, bot_name, provider_func):
        self.broker_dict[bot_name] = provider_func
    def broker(self, bot_name, config_obj):
        if (bot_name in self.broker_dict):
            return self.broker_dict[bot_name](config_obj)
        else:
            raise AttributeError("Provider for '%s' not known to the Bot Broker." % bot_name)