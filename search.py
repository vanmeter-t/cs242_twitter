"""
CS242 Twitter Streaming - Project Part A
Trevor Van Meter
tvanm001
860835689
"""

import os, sys, lucene, settings, csv

from datetime import datetime

from java.nio.file import Paths
from java.lang import System
from java.text import DecimalFormat
from java.util import Arrays

from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, TermQuery, MatchAllDocsQuery
from org.apache.lucene.index import (IndexWriter, IndexReader, DirectoryReader, Term, IndexWriterConfig)
from org.apache.lucene.document import Document, Field, TextField

TITLE = "title"
TEXT = "text"
searchValues = ['Torrey Pines']

class Searcher(object):

    def searchWithTerm(cls, term, indexReader):
        analyzer = StandardAnalyzer()
        query = QueryParser(TEXT, analyzer).parse(term)

        hitsPerPage = 50
        start = datetime.now()
        searcher = IndexSearcher(indexReader)
        scoreDocs = searcher.search(query, hitsPerPage).scoreDocs
        duration = datetime.now() - start
        print("%s total matching documents in %s:" % (len(scoreDocs), duration))

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)

            print(doc.get(TITLE))
            for idx, val in enumerate(settings.HEADERS):
                print('   ', val, ':', doc.get(val))
            print("\n------------------------------------------------------")
            
        print("\n------------------------------------------------------")

    searchWithTerm = classmethod(searchWithTerm)

class LuceneSearcher(object):

    def __init__(self, directory):
        self.directory = directory
        self.indexDir = FSDirectory.open(Paths.get(os.path.join(self.directory, settings.INDEX_DIR)))
    
    def runSimple(self):
        indexReader = DirectoryReader.open(self.indexDir)

        for term in searchValues:
            print("\nsearch by term '%s' ..." % term)
            Searcher.searchWithTerm(term, indexReader)

        indexReader.close()

    def run(cls, argv):
        #lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        baseDir = os.path.dirname(os.path.abspath(argv[0]))
        example = LuceneSearcher(baseDir)
        example.runSimple()
         
    run = classmethod(run)