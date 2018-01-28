"""pylucene indexer"""

import os, sys, lucene, settings, csv

from java.nio.file import Paths
from java.lang import System
from java.text import DecimalFormat
from java.util import Arrays

from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.search import IndexSearcher, TermQuery, MatchAllDocsQuery
from org.apache.lucene.store import FSDirectory, SimpleFSDirectory
from org.apache.lucene.index import (IndexWriter, IndexReader, DirectoryReader, Term, IndexWriterConfig)
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.facet import DrillSideways, DrillDownQuery
from org.apache.lucene.facet import (Facets, FacetField, FacetResult, FacetsConfig, FacetsCollector)
from org.apache.lucene.facet.taxonomy import FastTaxonomyFacetCounts
from org.apache.lucene.facet.taxonomy.directory import (DirectoryTaxonomyWriter, DirectoryTaxonomyReader)

TITLE = "title"
TEXT = "text"

class Indexer(object):

    def index (cls, indexDir):
        config = IndexWriterConfig(WhitespaceAnalyzer())
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(indexDir, config)
        
        file = open(settings.CSV_NAME) # open in read mode

        with open(settings.CSV_NAME) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(readCSV):
                if i > 0:
                    doc = Document() # create a new document
                    for idx, val in enumerate(row):
                        doc.add(TextField(TITLE, settings.HEADERS[idx], Field.Store.YES))
                        doc.add(TextField(TEXT, val, Field.Store.NO))
                    writer.addDocument(doc) # add the document to the IndexWriter
                
        writer.close()

    index = classmethod(index)

class LuceneIndexer(object):

    def __init__(self, directory):
        self.directory = directory
        self.indexDir = FSDirectory.open(Paths.get(os.path.join(self.directory, settings.INDEX_DIR)))

    def createIndex(self):
        Indexer.index(self.indexDir)

    def main(cls, argv):
        baseDir = os.path.dirname(os.path.abspath(argv[0]))
        example = LuceneIndexer(baseDir)
        example.createIndex()
        
            
    main = classmethod(main)

if __name__ == '__main__':
    print("lucene version is:", lucene.VERSION)
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    LuceneIndexer.main(sys.argv)