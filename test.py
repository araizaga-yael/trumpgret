import tweepy
consumer_key = "arijIsWxBAZVpHIl1pWaCHRuW"
consumer_secret = "mAQeIQD6H07LXY0S4Rfoi4Wo3BCTbSWRg4a7mWBrMFWJ9iPHZe"
access_token = "931246988695351300-qd0An9bZLY5fITsyFAhoqeltWRFSTNo"
access_token_secret = "fZvf26nvvlJySOgEINeB5CwiEHBDHr7H4bSPUHpseSDOO"

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth) 

# Using the API object to get tweets from your timeline, and storing it in a variable called public_tweets
public_tweets = api.home_timeline()

#print("\nMy tweets")
# foreach through all tweets pulled
#for tweet in public_tweets:
    # printing the text stored inside the tweet object
    #if(tweet.retweeted)
#    originaltTweet = api.get_status(tweet.id_str)
#    print(originaltTweet.retweeted_status.created_at)

print("\n\nTrumpgret")

trumpgrets = api.user_timeline(screen_name = 'Trump_Regrets', count = 5, include_rts = True)
for tweet in trumpgrets:
    originaltTweet = api.get_status(tweet.id_str)
    print(originaltTweet.retweeted_status.created_at)