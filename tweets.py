import tweepy, os, sys
from keys import consumer_key, consumer_secret

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth)


def get_tweets(screen_name):
    tweets = []
    tweets.extend(api.user_timeline(screen_name=screen_name, count=300, tweet_mode='extended'))
    tweets_rt_filtered = list(filter(lambda tweet: tweet.full_text[0:2] != "RT", tweets))
    tweets_links_removed = list(map(lambda tweet: " ".join(tweet.full_text.split(" ")[:-1]), tweets_rt_filtered))
    with open(os.path.join(os.getcwd(), "data/", "trump.txt"), "w") as out:
        for i in range(len(tweets_links_removed)):
            out.write(tweets_links_removed[i])
            while i + 1 < len(tweets_links_removed) and tweets_links_removed[i + 1][0:4] == '....':
                out.write(' ' + tweets_links_removed[i + 1][4:])
                i += 1
            out.write('\n\n')

def main():
    if len(sys.argv) < 2:
        print("usage: python tweets.py ")
    get_tweets(sys.argv[1])

if __name__ == '__main__':
    main()
