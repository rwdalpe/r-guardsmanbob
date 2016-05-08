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

from praw import Reddit

from gbobstatusbot.reddit.reddit_wrapper import RedditWrapper, PasswordGrantRedditWrapperDecorator


def get_reddit_wrapper(config_obj):
    return PasswordGrantRedditWrapperDecorator(RedditWrapper(__create_gbobstatusbot_reddit_instance(config_obj)),
                                               config_obj)


def __create_gbobstatusbot_reddit_instance(config_obj):
    user_agent = config_obj.UserAgent()
    r = Reddit(user_agent, disable_update_check=True)
    r.set_oauth_app_info(config_obj.ClientID(), config_obj.ClientSecret(), "http://example.org/garbageuri")
    return r
