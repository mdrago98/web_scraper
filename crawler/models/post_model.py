from datetime import datetime
from re import compile as reg_compile


class PostModel:
    """
    A class that represents a user post from social media
    """

    def __init__(self, post_id: str, title: str, content: str, url: str, score: int,
                 created_date: int, scope: str, has_external: bool):
        """
        Initialises the post class
        :param post_id: he post id
        :param title: the title
        :param content: the content
        :param url: the post url
        :param score: the number of likes/ upvotes/ retweets
        :param created_date: a numeric representation of the date the post was created
        :param scope: the origin scope of the post
        :param has_external: a flag indicating if the post has external links
        """
        self.post_id: str = self.get_id(scope, post_id)
        self.title: str = title
        self.content: str = content
        self.url: str = url
        self.score: int = score
        self.created_date: datetime = datetime.fromtimestamp(created_date)
        self.has_external: bool = has_external

    url_regex = reg_compile(r'^(https?://)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*/?')

    @staticmethod
    def get_id(source, post_id) -> str:
        """
        A function to generate a new id
        :param source: the source from which the post was obtained
        :param post_id: the post id
        :return: the new id
        """
        return f'{source}_{post_id}'

    def get_links(self) -> list:
        """
        A function to check if the content has a link
        https://www.google.com
        http://www.google.com
        www.google.com
        www.google239.com/ayy/lmao?=123
        :return: true IFF the content has a link
        """
        return list(self.url_regex.findall(self.content))

    def as_dict(self):
        """
        A utility function to get the dict representation of the post object
        :return:
        """
        dict_object = dict((key, value) for key, value in self.__dict__.items()
                           if not callable(value) and not key.startswith('__'))
        dict_object['_id'] = self.post_id
        return dict_object
