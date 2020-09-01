import praw

from crawler.models.post_model import PostModel
from crawler.web_handlers.source_handler import SourceHandler, ApiHandlerMixin


class RedditSourceHandler(ApiHandlerMixin, SourceHandler):
    """
    A class that represents a reddit source handler
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        limit: int = 1000,
        strategy: str = "search",
        sub_reddit="all",
    ):
        """
        Inits a reddit source handler
        :param client_id: the client id
        :param client_secret: the client secret
        :param user_agent: the user agent
        """
        super().__init__(client_id, client_secret, user_agent)
        self.sub_reddit = sub_reddit
        self.api = praw.Reddit(
            client_id=client_id, client_secret=client_secret, user_agent=user_agent
        )
        self.strategy = strategy
        self.sub_reddit = self.api.subreddit(self.sub_reddit)
        self.limit = limit

    def get_posts(self, query):
        """
        Gets posts for a subreddit
        :param query: the query
        :return: returns a list of posts
        """
        post_gen_fun = getattr(self.sub_reddit, self.strategy)(
            query=query, limit=self.limit
        )
        return [
            PostModel(
                post.id,
                post.title,
                post.selftext,
                post.url,
                post.score,
                post.created_utc,
                "REDDIT",
                not post.is_self,
            )
            for post in post_gen_fun
        ]
