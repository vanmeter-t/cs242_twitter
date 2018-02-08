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
                id_str = status.id_str
                name = status.user.screen_name
                created = status.created_at
                loc = status.user.location
                mentions = status.entities.get('user_mentions')
                hashtags = status.entities.get('hashtags')
                text = status.text

                try:
                    try:
                        csvWriter.writerow([id_str, name.encode('utf-8'), created, loc, mentions.encode('utf-8'), hashtags.encode('utf-8'), text.encode('utf-8')])
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

    def write(self, csvFile, results):
        global csvWriter
        global totalCount 
        global maxCount
        global stream

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
        
            
    write = classmethod(write)

    def run(self, argv):
        global csvWriter
        global totalCount 
        global maxCount
        global stream

        auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
        auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        try:
            os.remove(argv["generateFile"])
        except Exception as err:
            print("try remove: .csv file not found") # do nothing

        csvFile = open(argv["generateFile"], 'a')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(settings.HEADERS)

        if not argv["searchTwitter"]:
            # STREAM ~ set subclass StreamListener for tweepy
            global stream
            stream_listener = StreamListener()
            stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
            stream.filter(languages=["en"])
        else:
            # USER/QUERY SEARCH
            lastId = -1
            totalCt = 0
            language = "en" # Language code (follows ISO 639-1 standards)
            query = argv["searchTwitter"] # The search term you want to find
            maxCount = int(argv["maxTweetCount"])
            print("Searching Twitter for " + query)

            while totalCt < maxCount:
                count = maxCount - totalCt
                try:
                    newTweets = api.search(q=query, lang=language, count=count, max_id=str(lastId - 1))
                    if not newTweets:
                        break
                    self.write(csvFile, newTweets)
                    totalCt += len(newTweets)
                    lastId = newTweets[-1].id
                except tweepy.TweepError as e:
                    print("Tweepy Error: " + e)
                    break
            
            print("Results found: " + str(totalCt))

        csvFile.close()

    run = classmethod(run)

