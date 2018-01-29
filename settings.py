"""
CS242 Twitter Streaming - Project Part A
Trevor Van Meter
tvanm001
860835689
"""

CONNECTION_STRING = "sqlite:///tweets.db"
TABLE_NAME = "tweets"
CSV_NAME = "tweets.csv"
INDEX_DIR = "indexer.tweets"
HEADERS = ["description", "loc", "name", "user_created", "followers", "id_str", "created", "text"]

try:
    from private import *
except Exception:
    pass