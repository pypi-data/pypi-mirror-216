import requests

from data_understand.constants import URLS


class TestURLs:
    def test_urls(self):
        for key in URLS:
            response = requests.get(URLS[key])
            assert response.status_code == 200
