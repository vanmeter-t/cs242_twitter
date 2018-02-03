"""
CS242 Twitter Streaming - Project Part A
Trevor Van Meter
tvanm001
860835689
"""
import sys
from importer import *
from indexer import *
from search import *

class Main(object):
    def run(cls, argv):

        args = { "main" : argv[0]}
        for idx, arg in enumerate(argv):
            if idx % 2 != 0:
                # define the function blocks
                if arg == "--generateFile":
                    args["generateFile"] = argv[idx+1]
                    args["file"] = argv[idx+1]
                elif arg == "--file":
                    args["generateFile"] = ""
                    args["file"] = argv[idx+1]

                if arg == "--search":
                    print("--search" + argv[idx+1])
                    args["search"] = argv[idx+1]
                else:
                    args["search"] = ""

                if arg == "--searchTwitter":
                    args["searchTwitter"] = argv[idx+1]
                else:
                    args["searchTwitter"] = ""

                if arg == "--skipIndex":
                    args["skipIndex"] = argv[idx+1]
                else:
                    args["skipIndex"] = False

        if args["generateFile"] != "":
            Importer.run(args)

        if not args["skipIndex"]:
            LuceneIndexer.run(args)
        else:
            lucene.initVM(vmargs=['-Djava.awt.headless=true'])

        if args["search"] != "":
            LuceneSearcher.run(args)
        else:
            print("No search term provided by --search")

    run = classmethod(run)

if __name__ == '__main__':
    Main.run(sys.argv)