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
