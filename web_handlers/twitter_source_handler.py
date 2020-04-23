from models.post_model import PostModel
from web_handlers.source_handler import SourceHandler, ResourceDownloaderMixin, ParserMixin
import json


class TwitterSourceHandler(ResourceDownloaderMixin, ParserMixin, SourceHandler):
    """
    A class that represents a reddit source handler
    """

    @property
    def twitter_url_template(self):
        return 'https://twitter.com/i/profiles/show/{}/timeline/tweets?' \
               + 'include_available_features=1&include_entities=1&include_new_items_bar=true'

    def __init__(self):
        """
        Inits a twitter source handler
        """
        super().__init__()

    @staticmethod
    def get_headers(query) -> dict:
        """
        A function to generate the headers to get the
        :param query:
        :return:
        """
        return {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": f"https://twitter.com/{query}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
            "X-Twitter-Active-User": "yes",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Language": "en-US",
        }

    @staticmethod
    def get_score(tweet) -> int:
        interactions = [interaction.text for interaction in tweet.select('span.ProfileTweet-actionCount')]
        return int(interactions[2].split()[0].replace(',', "").replace('.', ""))

    def get_posts(self, query, limit: int = 10000):
        """
        Gets posts for a subreddit
        :param query: the query
        :param limit: the limit
        :return: returns a list of posts
        """
        res = self.get_resource(
            self.twitter_url_template.format(query),
            headers=self.get_headers(query))
        parser = self.configure_parser(json.loads(res)['items_html'], 'html5lib')
        return [PostModel(tweet.attrs['data-item-id'], '',
                          ' '.join(next(iter(tweet.select('p.tweet-text')), '').text.split()),
                          user.attrs['data-permalink-path'], self.get_score(tweet),
                          int(int(''.join(tweet.select('span._timestamp')[0].attrs['data-time-ms'].split())) / 1000),
                          'TWITTER', False)
                for tweet, user in
                zip(
                    parser.select('li.stream-item'),
                    parser.select('div.js-profile-popup-actionable')
                )]
