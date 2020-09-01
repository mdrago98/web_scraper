from abc import ABC, abstractmethod
from typing import Optional

import requests
from bs4 import BeautifulSoup


class SourceHandler(ABC):
    """
    An abstract class representing a source handler
    """

    @abstractmethod
    def get_posts(self, query) -> list:
        """
        A function to get all posts related to a company
        :param query: the
        :return:
        """
        pass


class ApiHandlerMixin:
    """
    A mix in class that adds api handling functionality
    """

    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent


class ResourceException(Exception):
    """
    A class representing a resource exception
    """

    def __init__(self, status_code: int, reason: str):
        """
        Initialises the exception
        :param status_code: the status code
        :param reason: the reason message
        """
        # Call the base class constructor with the parameters it needs
        super().__init__(f"The resource responded with {status_code} {reason}")


class ResourceDownloaderMixin:
    """
    A mix-in to download online resources
    """

    def get_resource(self, url, headers: dict) -> Optional[bytes]:
        """
        A function to get a resource from the internet
        :param url: the url
        :param headers: a dictionary containing the headers
        :return: <optional> byte representation if the resource is found
        """
        page = requests.get(url, headers=headers)
        if page.status_code is not 200:
            raise ResourceException(page.status_code, page.reason)
        return page.content


class ParserMixin:
    """
    A mix-in to get parser support
    """

    def configure_parser(self, content: bytes, parser="html5lib"):
        """
        A function to initialise a new beautiful soup parser
        :param content: the content to parse
        :param parser: the parser type (html.parser(built-in), lxml, html5lib)
        :return:
        """
        return BeautifulSoup(content, parser)
