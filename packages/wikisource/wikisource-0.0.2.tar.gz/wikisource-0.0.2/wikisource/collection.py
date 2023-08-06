from .source import WikiSource
from typing import List

class SourceCollection:
    def __init__(self, 
                 sources: List[WikiSource], 
                 download_folder="/tmp"):
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
        results = list()
        for source in self.sources:
            source_results = source.search(query, num_max_results_per_source, num_max_results_per_chapter)
            for result in source_results:
                if num_max_results is None or len(results) < num_max_results:
                    results.append((source.author, source.title, result[0], result[1], result[2]))
        return results

