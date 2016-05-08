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