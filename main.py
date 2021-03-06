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

        args = { "main" : argv[0], 
                "generateFile": "",
                "file": "",
                "searchIndex": "",
                "searchTwitter": "", 
                "skipIndex": False,
                "maxTweetCount": 1000,
                "customPhrases": []
            }

        for idx, arg in enumerate(argv):
            if idx % 2 != 0:
                # define the function blocks
                if arg == "--generateFile":
                    args["generateFile"] = argv[idx+1]
                    args["file"] = argv[idx+1]
                
                if arg == "--file":
                    args["generateFile"] = ""
                    args["file"] = argv[idx+1]

                if arg == "--searchIndex":
                    args["searchIndex"] = argv[idx+1]

                if arg == "--searchTwitter":
                    args["searchTwitter"] = argv[idx+1]
                
                if arg == "--skipIndex":
                    args["skipIndex"] = argv[idx+1]

                if arg == "--maxTweetCount":
                    args["maxTweetCount"] = argv[idx+1]

                if arg == "--customPhrases":
                    args["customPhrases"] = argv[idx+1].split(",")
        
        if args["generateFile"] != "":
            Importer.run(args)
        else:
            print("Using existing file")

        if not args["skipIndex"]:
            LuceneIndexer.run(args)
        else:
            print("Skipped indexing")
            lucene.initVM(vmargs=['-Djava.awt.headless=true'])

        if args["searchIndex"] != "":
            LuceneSearcher.run(args)
        else:
            print("Skipped search, No search term provided by --searchIndex")

    run = classmethod(run)

if __name__ == '__main__':
    Main.run(sys.argv)