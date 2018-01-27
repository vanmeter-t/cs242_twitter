"""
CS242 Twitter Streaming - Project Part A
Trevor Van Meter
tvanm001
860835689
"""
import json
import dataset
import tweepy
import settings

db = dataset.connect(settings.CONNECTION_STRING)

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

        except AttributeError:
            return
            
    def on_error(self, status_code):
        if status_code == 420:
            return False

# setup tweepy with Twitter API Keys/Secrets
auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

# set subclass StreamListener for tweepy 
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS)