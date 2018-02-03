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

        if argv[3] != "--skipImporter":
            Importer.run(sys.argv)

        if len(argv) <= 4 or argv[4] != "--skipIndexer":
            LuceneIndexer.run(sys.argv)
        else:
            lucene.initVM(vmargs=['-Djava.awt.headless=true'])

        LuceneSearcher.run(sys.argv)
    run = classmethod(run)

if __name__ == '__main__':
    Main.run(sys.argv)