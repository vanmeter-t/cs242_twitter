"""
CS242 Twitter Streaming - Project Part A
Trevor Van Meter
tvanm001
860835689
"""
CSV_NAME = "tweets.csv"
INDEX_DIR = "indexer.tweets"
HEADERS = ["id_str", "name", "created", "loc", "mentions", "hashtags", "text"]

try:
    from private import *
except Exception:
    pass