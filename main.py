"""
CS242 Twitter Streaming - Project Part A
Trevor Van Meter
tvanm001
860835689
"""
import json, dataset, tweepy, csv, settings, os
from tokenizer import *

db = dataset.connect(settings.CONNECTION_STRING)

global counter
counter = 0
global csvFileCt
csvFileCt = 1

class StreamListener(tweepy.StreamListener):
    """Sub-class StreamListener for tweepy"""

    
    def on_status(self, status):

        #print(status)

        try:
            description = status.user.description
            loc = status.user.location
            text = status.text
            name = status.user.screen_name
            user_created = status.user.created_at
            followers = status.user.followers_count
            id_str = status.id_str
            created = status.created_at
            retweets = status.retweet_count

            table = db[settings.TABLE_NAME]
            try:
                # TODO: how to handle hashtags, emoji, foreign characters, translations?
                # TODO: extract out user tags, hashtags, location
                """
                 Content-based
                    – car, woman, sky
                • Context-based
                    – new york city, empire state building
                • Attribute
                    – nikon (type of camera), black and white (type of movie), homepage (type of web page)
                • Subjective
                    – pretty, amazing, awesome
                • Organizational
                """
                table.insert(dict(
                    user_description=description,
                    user_location=loc,
                    text=text,
                    user_name=name,
                    user_created=user_created,
                    user_followers=followers,
                    id_str=id_str,
                    created=created,
                    retweet_count=retweets
                ))
                global counter
                counter += 1
            except Exception as err:
                print(err)

        except AttributeError:
            return

        #dump 100,000 records to a CSV file 
        if counter == 100000:
            result = db[settings.TABLE_NAME].all()
            global csvFileCt
            dataset.freeze(result, format='csv', filename=settings.CSV_NAME + "_" + csvFileCt)
            csvFileCt += 1

    def on_error(self, status_code):
        if status_code == 420:
            return False

# setup tweepy with Twitter API Keys/Secrets
auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

try:
    os.remove(settings.CSV_NAME)
    os.remove(settings.TABLE_NAME + ".db")
except Exception as err:
    print() # do nothing

csvFile = open(settings.CSV_NAME, 'a')
csvWriter = csv.writer(csvFile)

# set subclass StreamListener for tweepy 
# stream_listener = StreamListener()
# stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
# stream.sample()

language = "en" # Language code (follows ISO 639-1 standards)
query = "Tiger Woods" # The search term you want to find
name = "nytimes" # The Twitter user who we want to get tweets from
tweetCount = 20 # Number of tweets to pull

#results = api.user_timeline(id=name, count=tweetCount)
results = api.search(q=query, lang=language)

#write out to database table
table = db[settings.TABLE_NAME]

#write csv header row
csvWriter.writerow(settings.HEADERS)

for tweet in results:
    #print(tweet.hashtags)
    #print(tokenize(tweet.text)) # tokenize
    description = tweet.user.description
    loc = tweet.user.location
    text = tweet.text
    name = tweet.user.screen_name
    user_created = tweet.user.created_at
    followers = tweet.user.followers_count
    id_str = tweet.id_str
    created = tweet.created_at
    retweets = tweet.retweet_count
    try:
        csvWriter.writerow([description, loc, name, user_created, followers, id_str, created, text.encode('utf-8')])
        table.insert(dict(
            user_description=description,
            user_location=loc,
            text=text,
            user_name=name,
            user_created=user_created,
            user_followers=followers,
            id_str=id_str,
            created=created,
            retweet_count=retweets
        ))
    except Exception as err:
        print(err)