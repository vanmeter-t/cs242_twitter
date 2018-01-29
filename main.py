"""
CS242 Twitter Streaming - Project Part A
Trevor Van Meter
tvanm001
860835689
"""

from importer import *
from indexer import *
from search import *

class Main(object):

    def run(cls, argv):
        Importer.run(sys.argv)
        LuceneIndexer.run(sys.argv)
        LuceneSearcher.run(sys.argv)

    run = classmethod(run)

if __name__ == '__main__':
    Main.run(sys.argv)