import unittest, os
from wikisource.source import WikiSource

sources = dict(
    rousseau = "https://fr.wikisource.org/wiki/Les_Confessions_(Rousseau)",
    nietzsche = "https://fr.wikisource.org/wiki/L%E2%80%99Origine_de_la_Trag%C3%A9die",
    locke = "https://fr.wikisource.org/wiki/Trait%C3%A9_du_gouvernement_civil_(trad._Mazel)",
    spinoza = "https://fr.wikisource.org/wiki/Trait%C3%A9_th%C3%A9ologico-politique",
    descartes = "https://fr.wikisource.org/wiki/Discours_de_la_m%C3%A9thode_(%C3%A9d._Cousin)",
    spinoza_2 = "https://fr.wikisource.org/wiki/Court_Traité",
    thucydides = "https://fr.wikisource.org/wiki/Biblioth%C3%A8que_historique_et_militaire/Guerre_du_P%C3%A9loponn%C3%A8se"
)


class WhenUsingWikiSourceToListChapters(unittest.TestCase):
    def test_it_should_have_a_book_url(self):
        wiki_source = WikiSource(sources["rousseau"])
        self.assertEqual(wiki_source.url, sources["rousseau"])

    def test_it_should_list_all_chapters(self):
        wiki_source = WikiSource(sources["rousseau"])
        wiki_source.read()
        self.assertEqual(len(wiki_source.chapter_links), 13)

    def test_it_should_have_a_title_and_an_author(self): 
        wiki_source = WikiSource(sources["rousseau"])
        wiki_source.read()
        self.assertEqual(wiki_source.author, "Jean-Jacques Rousseau")
        self.assertEqual(wiki_source.title, "Les Confessions")

    def test_it_should_list_all_chapters_for_nietzsche(self):
        wiki_source = WikiSource(sources["nietzsche"])
        wiki_source.read()
        self.assertEqual(len(wiki_source.chapter_links), 29)

    def test_it_should_list_all_chapters_for_locke(self):
        wiki_source = WikiSource(sources["locke"])
        wiki_source.read()
        self.assertEqual(len(wiki_source.chapter_links), 23)

    def test_it_should_list_all_chapters_for_spinoza(self):
        wiki_source = WikiSource(sources["spinoza"])
        wiki_source.read()
        self.assertEqual(len(wiki_source.chapter_links), 22)

    def test_it_should_list_all_chapters_for_descartes(self):
        wiki_source = WikiSource(sources["descartes"])
        wiki_source.read()
        self.assertEqual(len(wiki_source.chapter_links), 6)

    def test_it_should_list_all_chapters_for_spinoza_2(self):
        wiki_source = WikiSource(sources["spinoza_2"])
        wiki_source.read()
        self.assertGreater(len(wiki_source.chapter_links), 0)

    def test_it_should_list_all_chapters_for_thucydides(self):
        wiki_source = WikiSource(sources["thucydides"])
        wiki_source.read()
        self.assertEqual(len(wiki_source.chapter_links), 10)


class WhenUsingWikiSourceToSearch(unittest.TestCase):
    def test_it_should_return_matching_paragraphs(self):
        wiki_source = WikiSource(sources["rousseau"])
        wiki_source.read()
        results = wiki_source.search("désir")
        self.assertEqual(len(results), 52)
        
        results = wiki_source.search("désir", num_max_sentences_per_chapter=1)
        self.assertEqual(len(results), 13)


