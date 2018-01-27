#settings
TRACK_TERMS = ["$ltc", "$appc", "$litecoin", "$lend"]
CONNECTION_STRING = "sqlite:///tweets.db"
CSV_NAME = "tweets.csv"
TABLE_NAME = "tweets"

try:
    from private import *
except Exception:
    pass