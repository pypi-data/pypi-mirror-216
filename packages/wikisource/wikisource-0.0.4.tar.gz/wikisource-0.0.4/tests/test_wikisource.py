import unittest, os
from wikisource.source import WikiSource

sources = dict(
    rousseau = dict(url="https://fr.wikisource.org/wiki/Les_Confessions_(Rousseau)",
                    title="Les Confessions"),
    nietzsche = dict(url="https://fr.wikisource.org/wiki/L%E2%80%99Origine_de_la_Trag%C3%A9die",
                     title="L'Origine de la Tragédie"),
    locke = dict(url="https://fr.wikisource.org/wiki/Trait%C3%A9_du_gouvernement_civil_(trad._Mazel)",
                 title="Traité du gouvernement civil"),
    spinoza = dict(url="https://fr.wikisource.org/wiki/Trait%C3%A9_th%C3%A9ologico-politique",
                   title="Traité théologico-politique"),
    descartes = dict(url="https://fr.wikisource.org/wiki/Discours_de_la_m%C3%A9thode_(%C3%A9d._Cousin)",
                     title="Discours de la méthode"))

class WhenUsingWikiSourceToListChapters(unittest.TestCase):
    def test_it_should_have_a_book_url(self):
        wiki_source = WikiSource(sources["rousseau"]["url"])
        self.assertEqual(wiki_source.url, sources["rousseau"]["url"])

    def test_it_should_list_all_chapters(self):
        wiki_source = WikiSource(sources["rousseau"]["url"])
        wiki_source.read()
        self.assertEqual(len(wiki_source.chapter_links), 13)

    def test_it_should_have_a_title_and_an_author(self): 
        wiki_source = WikiSource(sources["rousseau"]["url"])
        wiki_source.read()
        self.assertEqual(wiki_source.author, "Jean-Jacques Rousseau")
        self.assertEqual(wiki_source.title, "Les Confessions")

    def test_it_should_list_all_chapters_for_nietzsche(self):
        wiki_source = WikiSource(sources["nietzsche"]["url"])
        wiki_source.read()
        self.assertEqual(len(wiki_source.chapter_links), 29)

    def test_it_should_list_all_chapters_for_locke(self):
        wiki_source = WikiSource(sources["locke"]["url"])
        wiki_source.read()
        self.assertEqual(len(wiki_source.chapter_links), 23)

    def test_it_should_list_all_chapters_for_spinoza(self):
        wiki_source = WikiSource(sources["spinoza"]["url"])
        wiki_source.read()
        self.assertEqual(len(wiki_source.chapter_links), 22)

    def test_it_should_list_all_chapters_for_descartes(self):
        wiki_source = WikiSource(sources["descartes"]["url"])
        wiki_source.read()
        self.assertEqual(len(wiki_source.chapter_links), 6)



class WhenUsingWikiSourceToSearch(unittest.TestCase):
    def test_it_should_return_matching_paragraphs(self):
        wiki_source = WikiSource(sources["rousseau"]["url"])
        wiki_source.read()
        results = wiki_source.search("désir")
        self.assertEqual(len(results), 133)
        
        results = wiki_source.search("désir", num_max_sentences_per_chapter=1)
        self.assertEqual(len(results), 13)


