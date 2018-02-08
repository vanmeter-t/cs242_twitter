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
        super().__init__()
        self.offset = 0
        self.termAtt = self.addAttribute(CharTermAttribute.class_)
        self.offsetAtt = self.addAttribute(OffsetAttribute.class_)
        self.save = super().cloneAttributes()
        self.stack = []
        
    def incrementToken(self):        

        # if val == 35: # # Hashtag
        #     self.isHashtag = True

        # if val == 64: # @ Mention
        #     self.isMention = True

        if len(self.stack) > 0:
            saved = self.stack.pop()
            self.save.restoreState(saved)

        upto = 0;
        buffer = [];
        while True:
            length = self.input.read()
            if length == -1: 
                if len(buffer) > 0:
                    self.addToken("".join(buffer), upto);
                return False
            upto += 1;
            buffer.append(chr(length));
      
        self.addToken("".join(buffer));
        return True;

    def addToken(self, arg, upto):
        current = self.captureState()
        self.save.restoreState(current)
        self.termAtt = self.save.getAttribute(CharTermAttribute.class_)
        self.offsetAtt = self.save.getAttribute(OffsetAttribute.class_)
        self.termAtt.setEmpty()
        self.termAtt.append(arg)
        self.termAtt.setLength(upto)
        self.offsetAtt.setOffset(self.offset, self.offset + upto)
        self.offset += upto
        self.stack.append(self.save.captureState())

class CustomAnalyzer(PythonAnalyzer):
    def __init__(self):
        PythonAnalyzer.__init__(self)
        self.phrases = []

    def customPhrases(self, phrases):
        self.phrases = phrases

    def createComponents(self, fieldName):
        #source = StandardTokenizer()
        source = CustomTokenizer(lambda: self._reader)
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