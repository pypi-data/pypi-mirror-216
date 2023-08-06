from dataclasses import dataclass
import re

@dataclass
class Paragraph:
    """
    A paragraph of a chapter.
    """

    text: str

    def __post_init__(self):
        self.text = self.text.strip()
        self.sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', self.text)

    def search(self, query):
        """ Search for a query in the paragraph.

        :param query: The query to search for.
        :type query: str
        :return: A list of results.
        :rtype: List[SearchResult]
        """
        return [sentence for sentence in self.sentences if query in sentence]

