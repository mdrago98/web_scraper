from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock


from crawler.models.post_model import PostModel
from crawler.web_handlers import RedditSourceHandler


# 1583533583.0 utc
class MockSubmission:
    """
    A fake submission class to be used for testing
    """

    def __init__(
        self,
        id: str,
        title: str,
        selftext: str,
        url: str,
        score: int,
        created_utc: float,
        is_self: bool,
    ):
        self.id = id
        self.title = title
        self.selftext = selftext
        self.url = url
        self.score = score
        self.created_utc = created_utc
        self.is_self = is_self


class TestRedditSourceHandler(TestCase):
    """
    A test class containing unit tests for the reddit Source handler
    """

    def test_searches_reddit_and_returns_posts(self):
        def fake_submission(query, limit):
            yield MockSubmission(
                "id1test1", "test title", "self text", "test url", 2, 1583533583.0, True
            )

        sut = RedditSourceHandler("id", "secret", "agent")
        sut.api = MagicMock()
        sut.sub_reddit.search = fake_submission
        result = sut.get_posts("test")
        first_res: PostModel = result[0]
        self.assertEqual(1, len(result))
        self.assertEqual(
            {
                "post_id": "REDDIT_id1test1",
                "title": "test title",
                "content": "self text",
                "url": "test url",
                "score": 2,
                "created_date": datetime.fromtimestamp(1583533583),
                "has_external": False,
                "_id": "REDDIT_id1test1",
            },
            result[0].as_dict(),
        )
