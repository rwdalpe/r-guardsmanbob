import requests


class RedditWrapper:
    def __init__(self, r):
        self._r = r

    def get_username(self):
        me = self._r.get_me()
        return me.name


class PasswordGrantRedditWrapperDecorator(RedditWrapper):
    def __init__(self, decorated, config_obj):
        self.decorated = decorated
        self.config_obj = config_obj

    def get_username(self):
        self.__set_access_token()
        return self.decorated.get_username()

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
        return token
