import praw

from models.post_model import PostModel
from web_handlers.sourcehandler import SourceHandler


class RedditSourceHandler(SourceHandler):

    def __init__(self, client_id: str, client_secret: str, user_agent: str, strategy: str = 'search', sub_reddit='all'):
        """
        Inits a reddit source handler
        :param client_id: the client id
        :param client_secret: the client secret
        :param user_agent: the user agent
        """
        super().__init__(client_id, client_secret, user_agent)
        self.sub_reddit = sub_reddit
        self.api = praw.Reddit(client_id=client_id,
                               client_secret=client_secret,
                               user_agent=user_agent)
        self.strategy = strategy

    def get_posts(self, query, limit: int = 10000):
        """
        Gets posts for a subreddit
        :param query: the query
        :param limit: the limit
        :return: returns a list of posts
        """
        sub_reddit = self.api.subreddit(self.sub_reddit)
        post_gen_fun = getattr(sub_reddit, self.strategy)(query=query, limit=limit)
        return [PostModel(post.id, post.title, post.content, post.url, post.score, post.created) for post in post_gen_fun]


sh = RedditSourceHandler('OI2Xgj35GgGQRA', 'reb2V3ZGmJNhq3v8I-RJoWQeJZA', 'sentiment analysis')
sh.get_posts('teslamotors')

