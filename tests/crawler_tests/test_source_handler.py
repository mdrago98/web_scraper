from unittest import TestCase
from unittest.mock import patch


from crawler.web_handlers.source_handler import (
    ResourceDownloaderMixin,
    ResourceException,
)


class MockResponse:
    def __init__(self, content, status_code, reason=""):
        self.content = content
        self.status_code = status_code
        self.reason = reason


def mocked_requests_get():
    return MockResponse("loaded".encode("utf-8"), 200)


class TestResourceMixIn(TestCase):
    @patch(
        "requests.get",
        lambda *args, **kwargs: MockResponse("loaded".encode("utf-8"), 200),
    )
    def test_fetch_resource_fetches_resource(self):
        sut = ResourceDownloaderMixin()
        result = sut.get_resource("", {})
        self.assertEqual(
            result.decode("utf-8"),
            "loaded",
            "Resource handler did not get the correct message",
        )

    @patch("requests.get", lambda *args, **kwargs: MockResponse("", 404))
    def test_fetch_unknown_resource(self):
        sut = ResourceDownloaderMixin()
        self.assertRaises(ResourceException, sut.get_resource, "", {})
