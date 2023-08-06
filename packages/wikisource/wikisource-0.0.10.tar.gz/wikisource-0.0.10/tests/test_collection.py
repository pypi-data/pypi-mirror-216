import unittest, os
from wikisource.collection import SourceCollection
from wikisource.source import WikiSource

url_rousseau = "https://fr.wikisource.org/wiki/Les_Confessions_(Rousseau)"
url_nietzsche = "https://fr.wikisource.org/wiki/L%E2%80%99Origine_de_la_Trag%C3%A9die"
url_locke = "https://fr.wikisource.org/wiki/Trait%C3%A9_du_gouvernement_civil_(trad._Mazel)"
url_spinoza = "https://fr.wikisource.org/wiki/Trait%C3%A9_th%C3%A9ologico-politique"
url_descartes = "https://fr.wikisource.org/wiki/Discours_de_la_m%C3%A9thode_(%C3%A9d._Cousin)"

collection_urls = [url_rousseau, url_nietzsche, url_locke, url_spinoza, url_descartes]


class WhenUsingCollection(unittest.TestCase):
    def test_it_should_have_a_list_of_urls(self):
        collection = SourceCollection([WikiSource(url) for url in collection_urls])
        self.assertEqual(len(collection.sources), len(collection_urls))

    def test_it_should_read_all_sources(self):
        collection = SourceCollection([WikiSource(url) for url in collection_urls])
        collection.read()
        self.assertEqual(len(collection.sources), 5)

class WhenSearchingCollection(unittest.TestCase):
    def test_it_should_return_results(self):
        collection = SourceCollection([WikiSource(url) for url in collection_urls])
        collection.read()
        results = collection.search("désir", num_max_results_per_source=1)
        self.assertEqual(len(results), 5)

