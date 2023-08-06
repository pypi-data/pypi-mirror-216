# WikiSource

wikisource is a python package to help search the [Wikisource Books](https://wikisource.org/wiki/Main_Page)

It offers a few classes to help find sentences in a book, or in a book collection. 

For example, to search in a book for a specific string

```
from wikisource import WikiSource

book = WikiSource("https://fr.wikisource.org/wiki/Discours_de_la_m%C3%A9thode_(%C3%A9d._Cousin)"
book.search("bon sens")
```

To search in a collection of books, you can use: 

```
from wikisource import Collection, WikiSource

books = Collection([WikiSource("https://fr.wikisource.org/wiki/Discours_de_la_m%C3%A9thode_(%C3%A9d._Cousin)"),
                    WikiSource("https://fr.wikisource.org/wiki/Les_Confessions_(Rousseau)"),
                    WikiSource("https://fr.wikisource.org/wiki/L%E2%80%99Origine_de_la_Trag%C3%A9die")])

books.search("bon sens")
```


The first search takes longer due to the fact that every chapter of the book needs to be downloaded locally. The next searches are faster. 

