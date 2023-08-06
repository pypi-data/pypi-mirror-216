from dataclasses import dataclass
import re

@dataclass
class Paragraph:
    text: str

    def __post_init__(self):
        self.text = self.text.strip()
        self.sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', self.text)

    def search(self, query):
        return [sentence for sentence in self.sentences if query in sentence]

