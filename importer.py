"""
CS242 Twitter Streaming - Project Part A
Trevor Van Meter
tvanm001
860835689
"""
import json, tweepy, csv, settings, os
from tokenizer import *

global stream
global csvWriter
global totalCount
totalCount = 0

global maxCount

class StreamListener(tweepy.StreamListener):
    """Sub-class StreamListener for tweepy"""

    def on_status(self, status):
        try:
            global csvWriter
            global totalCount 
            global maxCount
            global stream

            # check the limit of downloaded tweets
            if totalCount > maxCount:
                stream.disconnect()

            tokens = tokenize(status.text) 
            if tokens[0] != 'RT':
                #print(tokens)

                # description = status.user.description
                # loc = status.user.location
                # text = status.text
                # user_created = status.user.created_at
                # followers = status.user.followers_count
                # created = status.created_at
                # retweets = status.retweet_count

                id_str = status.id_str
                name = status.user.screen_name
                created = status.created_at
                loc = status.user.location
                mentions = status.entities.get('user_mentions')
                hashtags = status.entities.get('hashtags')
                text = status.text

                try:
                    try:
                        csvWriter.writerow([id_str, name, created, loc, mentions, hashtags, text.encode('utf-8')])
                        totalCount += 1
                    except Exception as err:
                        print(err)
                except Exception as err:
                    print(err)

        except AttributeError:
            return

    def on_error(self, status_code):
        if status_code == 420:
            return False

class Importer(object):

    def run(cls, argv):
        global csvWriter
        global totalCount 
        global maxCount
        global stream

        # setup tweepy with Twitter API Keys/Secrets
        # using AppAuthHandler application level auth instead of OAuthHandler for higher query limits
        auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
        auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)

        # these two parameters will "auto-sleep" and wait so the Twitter rate limit isn't exceeded
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        try:
            os.remove(argv["generateFile"])
        except Exception as err:
            print("try remove: .csv file not found") # do nothing

        maxCount = int(argv["maxTweetCount"])

        csvFile = open(argv["generateFile"], 'a')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(settings.HEADERS)

        # STREAM ~ set subclass StreamListener for tweepy

        if not argv["searchTwitter"]:
            global stream
            stream_listener = StreamListener()
            stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
            stream.filter(languages=["en"])
        else:
            # USER/QUERY SEARCH
            language = "en" # Language code (follows ISO 639-1 standards)
            query = argv["searchTwitter"] # The search term you want to find
            print("Searching Twitter for " + query)
            results = api.search(q=query, lang=language, count=maxCount)

            for tweet in results:
                id_str = tweet.id_str
                name = tweet.user.screen_name
                created = tweet.created_at
                loc = tweet.user.location
                mentions = tweet.entities.get('user_mentions')
                hashtags = tweet.entities.get('hashtags')
                text = tweet.text
                try:
                    csvWriter.writerow([id_str, name, created, loc, mentions, hashtags, text.encode('utf-8')])
                except Exception as err:
                    print(err)
            
            csvFile.close()

    run = classmethod(run)

