import requests
from bs4 import BeautifulSoup

class WebPage:
    """A web page."""

    def __init__(self, url):
        """Initializes a web page object.

        :param url: The url of the web page.
        :type url: str
        """
        self.url = url

    def read_soup(self):
        """Reads the web page and creates a BeautifulSoup object."""

        resp = requests.get(self.url)
        self.soup = BeautifulSoup(resp.text, 'html.parser')
