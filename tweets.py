import tweepy
from keys import consumer_key, consumer_secret

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth)

def get_tweets(screen_name):

    tweets = []
    tweets.extend(api.user_timeline(screen_name=screen_name, count=300))
    tweets_rt_filtered = list(filter(lambda tweet: tweet.text[0:2] != "RT", tweets))
    tweets_links_removed = list(map(lambda tweet: " ".join(tweet.text.split(" ")[:-1]), tweets_rt_filtered))
    for tweet in tweets_links_removed:
        print(tweet,'\n')
    print(len(tweets_rt_filtered))
get_tweets('@realDonaldTrump')