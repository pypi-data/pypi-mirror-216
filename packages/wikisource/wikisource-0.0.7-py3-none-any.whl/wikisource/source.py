import re, os
import requests
from bs4 import BeautifulSoup
from .chapter import Chapter
from .webpage import WebPage
import json
from dataclasses import dataclass
from typings import Optional

@dataclass
class ChapterLink:
    title: str
    url: str


class WikiSource(WebPage):
    """A wikisource book.

    It is matching a wikisource web page which contains the table of contents of a book.
    """

    def __init__(self, url:str, download_folder:str="/tmp"):
        """Initializes a wikisource book object.

        :param url: The url of the book.
        :type url: str
        :param download_folder: (optional) The folder where the book will be downloaded.
        :type download_folder: str
        """

        super().__init__(url)
        self.book_id = url.split('/')[-1]
        self.download_folder = download_folder
        self.download_path = f"{self.download_folder}/{self.book_id}__info.txt"
        self.chapters = list()

    def read(self): 
        """Reads the book online or from the downloaded files."""

        self.read_info()
        self.read_chapters()

    def read_info(self):
        if os.path.exists(self.download_path):
            self.read_info_from_file()
        else:
            self.read_soup()
            self.read_title()
            self.read_author()
            self.get_chapter_links()
            self.save_info()

    def read_info_from_file(self):
        with open(self.download_path, 'r') as f:
            info = json.load(f)
            self.title = info['title']
            self.author = info['author']
            self.chapter_links = list(map(lambda c: ChapterLink(**c), info['chapter_links']))

    def save_info(self): 
        with open(self.download_path, 'w') as f:
            json.dump(dict(chapter_links=list(map(lambda c: c.__dict__, self.chapter_links)),
                           title=self.title, 
                           author=self.author), f)


    def read_chapters(self):
        for i, cl in enumerate(self.chapter_links):
            chapter = Chapter(cl.title, cl.url)
            chapter.read()
            self.chapters.append(chapter)

    def read_title(self):
        title = self.soup.find("h1")
        self.title = re.sub(r"\([^\)]*\)", "", title.text).strip() if title else None

    def read_author(self):
        author = self.soup.find("span", { "itemprop": "author" })
        self.author = author.text if author else None


    def get_chapter_links(self):
        subheader = self.soup.find('div', id='subheader')
        if subheader:
            subheader.decompose()
        self.chapter_links = list()
        for content_div in self.soup.find_all('div', class_='prp-pages-output'):
            a_tags = content_div.find_all('a')
            for a_tag in a_tags:
                href = a_tag.get('href')
                if href and href.startswith(f"/wiki/{self.book_id}") and not(re.match(r".*\.(djvu|svg).*", href)):
                    self.chapter_links.append(ChapterLink(url=f"https://fr.wikisource.org{href}", title=a_tag.text))


    def search(self, 
               query, 
               num_max_results:Optional[int]=None, 
               num_max_sentences_per_chapter:Optional[int]=None):
        """Search for a query in the book.

        :param query: The query to search for.
        :type query: str
        :param num_max_results: (optional) The maximum number of results to return.
        :type num_max_results: int
        :param num_max_sentences_per_chapter: (optional) The maximum number of sentences to return per chapter.
        :type num_max_sentences_per_chapter: int
        :return: A list of results.
        :rtype: List[SearchResult]
        """

        results = list()
        for i_chap, chapter in enumerate(self.chapters):
            chapter_results = chapter.search(query)
            for i_sent, sentence in enumerate(chapter_results):
                if ((num_max_sentences_per_chapter is None) or i_sent <= num_max_sentences_per_chapter - 1) and \
                        ((num_max_results is None) or len(results) < num_max_results):
                    chapter_link = self.chapter_links[i_chap]
                    results.append((chapter_link.title, chapter_link.url, sentence))
        return results
