import sys, getopt
from wikisource.source import WikiSource

HELP = """HELP:
wks -u <wikisource_book_url> -q <query>
"""

def main(argv=sys.argv[1:]):
    print("argv", argv)
    book_url = None
    query = None
    opts, args = getopt.getopt(argv,"hu:q:",["url=","query="])
    for opt, arg in opts:
        print(opt, arg)
        if opt == '-h':
            print(HELP)
            sys.exit()
        elif opt in ("-u", "--url"):
            book_url = arg
        elif opt in ("-q", "--query"):
            query = arg

    if book_url is None or query is None:
        print(HELP)
        sys.exit()
    else:
        print("Book URL: ", book_url, "Query: ", query)
        source = WikiSource(book_url)
        source.read()
        results = source.search(query)
        for result in results:
            print(result)


if __name__ == "__main__":
   main(sys.argv[1:])
