"""
CS242 Twitter Streaming - Project Part A
Trevor Van Meter
tvanm001
860835689
"""

import os, sys, lucene, settings, csv, ast

from customizers import *

from java.nio.file import Paths
from java.lang import System
from java.text import DecimalFormat
from java.util import Arrays

from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.search import IndexSearcher, TermQuery, MatchAllDocsQuery
from org.apache.lucene.index import (IndexWriter, IndexReader, DirectoryReader, Term, IndexWriterConfig)
from org.apache.lucene.document import Document, Field, TextField

TITLE = "title"
TEXT = "text"
global fileName
global customPhrases

class Indexer(object):

    def index (cls, indexDir):

        # Custom Analyzer
        global customPhrases
        customAnalyzer = CustomAnalyzer()
        customAnalyzer.customPhrases(customPhrases)
        config = IndexWriterConfig(customAnalyzer)
        
        # Standard Analyzer
        # config = IndexWriterConfig(StandardAnalyzer())

        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(indexDir, config)
        
        print("Begin indexing...")
        global fileName
        with open(fileName, encoding='utf-8') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(readCSV):
                if i > 0:
                    doc = Document() # create a new document
                    doc.add(TextField(TITLE, "tweet_" + str(i), Field.Store.YES))
                    try:
                        for idx, val in enumerate(row):
                            # if hashtag or use mention, break down each as a field value
                            if val:
                                if settings.HEADERS[idx] == "hashtags":
                                    obj = ast.literal_eval(val)
                                    for t in obj:
                                        doc.add(TextField(settings.HEADERS[idx], t.get('text'), Field.Store.YES))
                                elif settings.HEADERS[idx] == "mentions":
                                    obj = ast.literal_eval(val)
                                    for m in obj:
                                        doc.add(TextField(settings.HEADERS[idx], m.get('screen_name'), Field.Store.YES))
                                else:
                                    doc.add(TextField(settings.HEADERS[idx], val, Field.Store.YES))
                    except ValueError as err:
                        print(err) 
                    writer.addDocument(doc) # add the document to the IndexWriter
        writer.close()

    index = classmethod(index)

class LuceneIndexer(object):

    def __init__(self, directory):
        self.directory = directory
        self.indexDir = FSDirectory.open(Paths.get(os.path.join(self.directory, settings.INDEX_DIR)))
        
    def createIndex(self):
        Indexer.index(self.indexDir)

    def run(cls, argv):
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        baseDir = os.path.dirname(os.path.abspath(argv["main"]))
        
        global fileName
        fileName = argv["file"]

        global customPhrases
        customPhrases = argv["customPhrases"]
        
        example = LuceneIndexer(baseDir)
        example.createIndex()
                    
    run = classmethod(run)