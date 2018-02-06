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
from org.apache.lucene.analysis.pattern import *
from org.apache.lucene.analysis.tokenattributes import *
from org.apache.pylucene.analysis import *

class CustomTokenizer(PythonTokenizer):
    ALPHANUM = "ALPHANUM"

    def __init__(self, getReader):
        super(CustomTokenizer, self).__init__()
        self.getReader = getReader
        self.i = 0
        self.data = []

        self.termAttr = self.addAttribute(CharTermAttribute.class_)
        self.typeAttr = self.addAttribute(TypeAttribute.class_)
        self.offsetAttr = self.addAttribute(OffsetAttribute.class_)
        self.posIncrAttr = self.addAttribute(PositionIncrementAttribute.class_)
        self.save = self.cloneAttributes()

        self.stack = []

    def incrementToken(self):
        while True:
            reader = self.getReader()
            val = reader.read()

            if val == -1: #EOF
                self.add("".join(self.data))
                return False

            if val == 32: #SPACE
                self.add("".join(self.data))
                return False

            if len(self.stack) > 0:
                syn = self.stack.pop()
                self.restoreState(syn)
                return True

            self.data.append(chr(val))
            self.i += 1
    
    def add(self, arg):
        current = self.captureState()
        self.save.restoreState(current)

        self.termAttr = self.save.addAttribute(CharTermAttribute.class_)
        self.typeAttr = self.save.addAttribute(TypeAttribute.class_)
        self.posIncrAttr = self.save.addAttribute(PositionIncrementAttribute.class_)
        self.offsetAttr = self.addAttribute(OffsetAttribute.class_)

        self.termAttr.setEmpty()
        self.termAttr.append(arg)
        self.typeAttr.setType(self.ALPHANUM)
        self.posIncrAttr.setPositionIncrement(1)
        self.offsetAttr.setOffset(self.i, self.i+len(self.data))

        self.stack.append(self.save.captureState())

        self.data = []
        self.i = 0
                
class CustomAnalyzer(PythonAnalyzer):
    def __init__(self):
        PythonAnalyzer.__init__(self)
        self.phrases = []

    def customPhrases(self, phrases):
        self.phrases = phrases

    def createComponents(self, fieldName):
        source = StandardTokenizer()
        #source = CustomTokenizer(lambda: self._reader)
        filter = CustomFilter(source, self.phrases)   
        filter = LowerCaseFilter(filter)
        filter = StopFilter(filter, StopAnalyzer.ENGLISH_STOP_WORDS_SET)
        
        return self.TokenStreamComponents(source, filter)

    def initReader(self, fieldName, reader):
        self._reader = reader
        return reader

class CustomFilter(PythonTokenFilter):

    TOKEN_TYPE_PHRASE = "PHRASE"

    def __init__(self, input, allPhrases):
        super(CustomFilter, self).__init__(input)

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
        self.term1 = ""
        self.term2 = ""
        self.phraseStack = []

    def incrementToken(self):

        if not self.input.incrementToken():
            return False

        if len(self.phraseStack) > 0:
            syn = self.phraseStack.pop()
            self.restoreState(syn)
            return True
            
        for phrase in self.allPhrases:
            addPhrase = False
            term0 = self.termAttr.toString()
            if len(phrase)==2:
                if self.term1==phrase[1] and term0==phrase[0]:
                    addPhrase = True
            if len(phrase)==3:
                if self.term2==phrase[2] and self.term1==phrase[1] and term0==phrase[0]:
                    addPhrase = True
            if addPhrase:
                rPhrase = phrase
                rPhrase.reverse()
                self.addPhrase(" ".join(rPhrase))

        self.term2 = self.term1
        self.term1 = self.termAttr.toString()
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