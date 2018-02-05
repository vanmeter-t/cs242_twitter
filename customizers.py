"""
CS242 Twitter Streaming - Project Part A
Trevor Van Meter
tvanm001
860835689
"""

import sys, os, lucene
from datetime import datetime
from org.apache.lucene.analysis import *
from org.apache.lucene.analysis.core import *
from org.apache.lucene.analysis.en import *
from org.apache.lucene.analysis.standard import *
from org.apache.lucene.analysis.tokenattributes import *
from org.apache.pylucene.analysis import *

class CustomAnalyzer(PythonAnalyzer):
    def __init__(self):
        PythonAnalyzer.__init__(self)
        self.phrases = []

    def customPhrases(self, phrases):
        self.phrases = phrases

    def createComponents(self, fieldName):
        source = StandardTokenizer()
        filter = PhraseFilter(source, self.phrases)   
        filter = LowerCaseFilter(filter)
        filter = StopFilter(filter, StopAnalyzer.ENGLISH_STOP_WORDS_SET)
        
        return self.TokenStreamComponents(source, filter)

    def initReader(self, fieldName, reader):
        return reader

class PhraseFilter(PythonTokenFilter):
    '''
    PhraseFilter allows for matching user-defined phrases
    '''
    TOKEN_TYPE_PHRASE = "PHRASE"

    def __init__(self, input, allPhrases):
        super(PhraseFilter, self).__init__(input)

        self.synonymStack = []
        self.termAttr = self.addAttribute(CharTermAttribute.class_)
        self.typeAttr = self.addAttribute(TypeAttribute.class_)
        self.posIncrAttr = self.addAttribute(PositionIncrementAttribute.class_)
        self.save = input.cloneAttributes()
        self.input = input

        revSplitPhrases = []
        for p in allPhrases:
            psplit = p.split()
            psplit.reverse()
            revSplitPhrases.append(psplit)

        self.allPhrases = revSplitPhrases
        self.lag1 = ""
        self.lag2 = ""
        self.phraseStack = []

    def incrementToken(self):

        if len(self.phraseStack) > 0:
            syn = self.phraseStack.pop()
            self.restoreState(syn)
            return True

        if not self.input.incrementToken():
            return False

        for phrase in self.allPhrases:
            addPhrase = False
            lag0 = self.termAttr.toString()
            if len(phrase)==2:
                if self.lag1==phrase[1] and lag0==phrase[0]:
                    addPhrase = True
            if len(phrase)==3:
                if self.lag2==phrase[2] and self.lag1==phrase[1] and lag0==phrase[0]:
                    addPhrase = True
            if addPhrase:
                rPhrase = phrase
                rPhrase.reverse()
                self.addPhrase(" ".join(rPhrase))

        self.lag2 = self.lag1
        self.lag1 = self.termAttr.toString()
        return True

    def addPhrase(self, arg):
        current = self.captureState()
        self.save.restoreState(current)
        self.termAttr = self.save.addAttribute(CharTermAttribute.class_)
        self.typeAttr = self.save.addAttribute(TypeAttribute.class_)
        self.posIncrAttr = self.save.addAttribute(PositionIncrementAttribute.class_)
        self.termAttr.setEmpty()
        self.termAttr.append(arg)
        self.typeAttr.setType(self.TOKEN_TYPE_PHRASE)
        self.posIncrAttr.setPositionIncrement(0)
        self.phraseStack.append(self.save.captureState())