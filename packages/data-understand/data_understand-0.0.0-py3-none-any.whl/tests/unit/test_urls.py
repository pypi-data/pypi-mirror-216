import requests

from data_understand.constants import URLS


class TestURLs:
    def test_urls(self):
        for key in URLS:
            # TODO: Remove the if condition below once the
            # repo is public.
            if key == "data.understand":
                continue
            response = requests.get(URLS[key])
            assert response.status_code == 200
