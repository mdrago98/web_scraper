from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

from crawler.web_handlers import TwitterSourceHandler

import pathlib
from os import path


class TestTwitterSourceHandler(TestCase):
    """
    A test class containing unit tests for the reddit Source handler
    """

    test_headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": f"https://twitter.com/google",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
        "X-Twitter-Active-User": "yes",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "en-US",
    }

    test_twitter_url = (
        "https://twitter.com/i/profiles/show/google/timeline/tweets?"
        + "include_available_features=1&include_entities=1&include_new_items_bar=true"
    )

    def test_get_posts_parses_twitter_response(self):
        with open(
            path.join(pathlib.Path(__file__).parent.absolute(), "twitter_sample.json")
        ) as file:
            test_tweets: str = file.read()
        sut = TwitterSourceHandler()
        sut.get_resource = MagicMock()
        sut.get_resource.return_value = test_tweets
        result = sut.get_posts("google")
        first_post = {
            "post_id": "TWITTER_1249729054925873153",
            "title": "",
            "content": "Searches for “how to help” have never been higher. Here’s to those sacrificing so much to help so many. http://g.co/thankyouhelpers pic.twitter.com/xrNgbVZmGe",
            "url": "/Google/status/1249729054925873153",
            "score": 884,
            "created_date": datetime.fromtimestamp(1586793600),
            "has_external": False,
            "_id": "TWITTER_1249729054925873153",
        }
        self.assertEqual(len(result), 1, "get_posts should have return one tweet")
        self.assertEqual(
            first_post, result[0].as_dict(), "The expected result did not match"
        )
