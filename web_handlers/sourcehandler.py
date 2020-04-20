from abc import ABC, abstractmethod


class SourceHandler(ABC):
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """
        Inits the handler.
        :param client_id: the client id
        :param client_secret: the client secret
        :param user_agent: the user agent
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        pass

    @abstractmethod
    def get_posts(self, query) -> list:
        """
        A function to get all posts related to a company
        :param query: the
        :return:
        """
        pass
