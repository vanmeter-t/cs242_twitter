class _analyzer(PythonAnalyzer):
  def tokenStream(_self, fieldName, reader):
      class _tokenStream(PythonTokenStream):
          def __init__(self_):
              super(_tokenStream, self_).__init__()
              self_.TOKENS = ["1", "2", "3", "4", "5"]
              self_.INCREMENTS = [1, 2, 1, 0, 1]
              self_.i = 0
              self_.posIncrAtt = self_.addAttribute(PositionIncrementAttribute.class_)
              self_.termAtt = self_.addAttribute(TermAttribute.class_)
              self_.offsetAtt = self_.addAttribute(OffsetAttribute.class_)
          def incrementToken(self_):
              if self_.i == len(self_.TOKENS):
                  return False
              self_.termAtt.setTermBuffer(self_.TOKENS[self_.i])
              self_.offsetAtt.setOffset(self_.i, self_.i)
              self_.posIncrAtt.setPositionIncrement(self_.INCREMENTS[self_.i])
              self_.i += 1
              return True
          def end(self_):
              pass
          def reset(self_):
              pass
          def close(self_):
              pass
      return _tokenStream()