from dataclasses import dataclass
from typing import List
from .webpage import WebPage
from .paragraph import Paragraph
import re, os


class Chapter(WebPage):
    def __init__(self, title, url, download_folder="/tmp"):
        super().__init__(url)
        self.title = title
        self.paragraphs = list()
        self.download_folder = download_folder
        file_name = re.sub(r'[^a-zA-Z0-9]', '_', self.url)
        self.download_path = os.path.join(self.download_folder, file_name + ".txt")

    def read(self):
        self.paragraphs = [Paragraph(paragraph) for paragraph in self.read_chapter_paragraphs()]

    def search(self, query):
        results = list()
        for i, paragraph in enumerate(self.paragraphs):
            paragraph_results = paragraph.search(query)
            results += paragraph_results
        return results

    def clean_paragraph_text(self, text):
        return text.replace('\n', ' ').replace('\xa0', ' ').strip()

    def read_chapter_paragraphs(self):
        if os.path.exists(self.download_path):
            with open(self.download_path, 'r') as f:
                return f.read().split("\n")
        else:
            paragraphs = self.get_chapter_paragraphs()
            self.save_chapter_paragraphs(paragraphs)
            return paragraphs


    def get_chapter_paragraphs(self):
        self.read_soup()
        title = self.soup.find('h1', class_='firstHeading').text
        content = self.soup.find('div', id='mw-content-text')
        if content:
            paragraphs = content.find_all("p")
            texts = [self.clean_paragraph_text(p.text) for p in paragraphs]
            texts = [text for text in texts if len(text) > 0]
            return texts
        else:
            return []

    def save_chapter_paragraphs(self, texts):
        with open(self.download_path, 'w') as f:
            f.write('\n'.join(texts))
