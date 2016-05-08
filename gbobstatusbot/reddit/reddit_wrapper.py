import time

import requests


class RedditWrapper:
    def __init__(self, r):
        self._r = r

    def get_username(self):
        me = self._r.get_me()
        return me.name

    def get_subreddit(self, subreddit_name):
        return self._r.get_subreddit(subreddit_name)

    def get_settings(self, subreddit_name):
        return self._r.get_settings(subreddit_name)

    def update_settings(self, subreddit_name, **kwargs):
        return self._r.update_settings(subreddit_name, **kwargs)

    def edit_wiki_page(self, subreddit_name, page, content, reason=''):
        return self._r.edit_wiki_page(subreddit_name, page, content, reason)


class PasswordGrantRedditWrapperDecorator(RedditWrapper):
    def __init__(self, decorated, config_obj):
        self.decorated = decorated
        self.config_obj = config_obj

    def get_username(self):
        self.__set_access_token()
        return self.decorated.get_username()

    def get_subreddit(self, subreddit_name):
        self.__set_access_token()
        return self.decorated.get_subreddit(subreddit_name)

    def get_settings(self, subreddit_name):
        self.__set_access_token()
        return self.decorated.get_settings(subreddit_name)

    def update_settings(self, subreddit_name, **kwargs):
        self.__set_access_token()
        return self.decorated.update_settings(subreddit_name, **kwargs)

    def edit_wiki_page(self, subreddit_name, page, content, reason=''):
        self.__set_access_token()
        return self.decorated.edit_wiki_page(subreddit_name, page, content, reason)

    def __set_access_token(self):
        token = self.__get_access_token(self.config_obj)
        self.decorated._r.set_access_credentials("*", token)

    def __get_access_token(self, config_obj):
        user_agent = config_obj.UserAgent()
        username = config_obj.Username()
        password = config_obj.Password()
        client_id = config_obj.ClientID()
        client_secret = config_obj.ClientSecret()
        client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        post_data = {"grant_type": "password", "username": username, "password": password}
        headers = {"User-Agent": user_agent}
        response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data,
                                 headers=headers)
        token = response.json()["access_token"]
        time.sleep(2)
        return token
