import unittest
from wikisource.chapter import Chapter

class WhenSearchingChapter(unittest.TestCase):
    def test_it_should_return_matching_paragraphs(self):
        chapter = Chapter("L'origine de la tragédie", "https://fr.wikisource.org/wiki/L%E2%80%99Origine_de_la_Trag%C3%A9die/L%27Origine_de_la_Trag%C3%A9die")
        chapter.read()
        results = chapter.search("conscience")
        self.assertEqual(results[0], "C’est à leurs deux divinités des arts, Apollon et Dionysos, que se rattache notre conscience de l’extraordinaire antagonisme, tant d’origine que de fins, qui exista dans le monde grec entre l’art plastique apollinien et l’art dénué de formes, la musique, l’art de Dionysos.")   
        self.assertEqual(len(results), 16)
