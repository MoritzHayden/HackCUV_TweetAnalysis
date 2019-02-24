#extract_topic.py
#Damir Pulatov
#HackCU V
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import json
import pandas as pd


#Save tweets to file
tweets_list = []
    

#This is a basic listener that just saves received tweets to list
class StdOutListener(StreamListener):
    def __init__(self, api=None):
        super(StdOutListener, self).__init__()
        self.num_tweets = 0

    def on_data(self, data):
        js = json.loads(data)
        #filter out retweets
        self.num_tweets += 1
        if self.num_tweets < 20:
            tweets_list.append(js)
            return True
        else:
            return False
        
    def on_error(self, status):
        print (status)


def extract_topic(topic):

    # Variables that contains the user credentials to access Twitter API 
    ACCESS_TOKEN = '1099382652195418112-HSenFzNQCjm1Q8IRRRe1yHKxqoySxT'
    ACCESS_SECRET = '7THNM3M0SBv9JaLBqG4dv6VTTGcRtX8vekDYw5y0RmrhM'
    CONSUMER_KEY = '7vprWYtinMgCD31IlIr45eBmn'
    CONSUMER_SECRET = 'jgbp8HpFm18u79lAiNY8LYEf7NaH7NQ43QcTR8wvidQrwdEHx4'

    # Setup tweepy to authenticate with Twitter credentials:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Create the api to connect to twitter with your creadentials
    api = tweepy.API(auth, retry_count=10, retry_errors= 429, retry_delay=30, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=[topic], languages=["en"])

    #get tweets' texts
    tweets = []
    for entry in tweets_list:
        tweets.append(entry['text'])

    #save tweets to file
    file_name = topic + "tweets"
    with open(file_name, 'w') as file:
        for item in tweets:
            file.write("%s\n" % item)

