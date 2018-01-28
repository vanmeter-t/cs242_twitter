""" tokenizer regex english-language """
import re, sys

emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)
 
regex_str = [
    r'<[^>]+>', # HTML
    r'(?:@[\w_]+)', # mentions "@mention"
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hashtags "#hashtag"
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # links (URL)
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # dash and single quote words
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s, lowercase=False):
    tokens = tokens_re.findall(s)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens