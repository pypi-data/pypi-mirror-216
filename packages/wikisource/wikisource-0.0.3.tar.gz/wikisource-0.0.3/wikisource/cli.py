import sys, getopt
from wikisource.source import WikiSource

HELP = """
wks -u <wikisource_book_url> -q <query>
"""

def main(argv=sys.argv):
    print("argv", argv)
    book_url = None
    query = None
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
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
        source = WikiSource(book_url)
        source.read()
        source.search(query)


if __name__ == "__main__":
   main(sys.argv[1:])
