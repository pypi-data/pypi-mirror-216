from .source import WikiSource
from typing import List

class SourceCollection:
    """ A collection of wikisource sources

    """


    def __init__(self, 
                 sources: List[WikiSource], 
                 download_folder="/tmp"):
        """ Initializes a source collection object.

        :param sources: The list of sources.
        :type sources: List[WikiSource]
        :param download_folder: (optional) The folder where the sources will be downloaded.
        :type download_folder: str
        """
        self.download_folder = download_folder
        self.sources = sources

    def read(self):
        for source in self.sources:
            source.read()

    def search(self, 
               query: str,
               num_max_results:int=None, 
               num_max_results_per_source:int=None, 
               num_max_results_per_chapter:int=None):
        """ Search for a query in the sources.

        :param query: The query to search for.
        :type query: str
        :param num_max_results: (optional) The maximum number of results to return.
        :type num_max_results: int
        :param num_max_results_per_source: (optional) The maximum number of results to return per source.
        :type num_max_results_per_source: int
        :param num_max_results_per_chapter: (optional) The maximum number of results to return per chapter.
        :type num_max_results_per_chapter: int
        :return: A list of results.
        :rtype: List[SearchResult]
        """

        results = list()
        for source in self.sources:
            source_results = source.search(query, num_max_results_per_source, num_max_results_per_chapter)
            for result in source_results:
                if num_max_results is None or len(results) < num_max_results:
                    results.append((source.author, source.title, result[0], result[1], result[2]))
        return results

