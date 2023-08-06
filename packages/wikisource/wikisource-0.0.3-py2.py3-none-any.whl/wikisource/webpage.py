import requests
from bs4 import BeautifulSoup

class WebPage:
    def __init__(self, url):
        self.url = url

    def read_soup(self):
        resp = requests.get(self.url)
        self.soup = BeautifulSoup(resp.text, 'html.parser')
