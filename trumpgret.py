import tweepy
import sqlite3

#Twitter account keys
consumer_key = "arijIsWxBAZVpHIl1pWaCHRuW"
consumer_secret = "mAQeIQD6H07LXY0S4Rfoi4Wo3BCTbSWRg4a7mWBrMFWJ9iPHZe"
access_token = "931246988695351300-qd0An9bZLY5fITsyFAhoqeltWRFSTNo"
access_token_secret = "fZvf26nvvlJySOgEINeB5CwiEHBDHr7H4bSPUHpseSDOO"

#setting up tweepy api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth) 

def getAllTweets(screenName):
    allTweets = []
    
    newTweets = api.user_timeline(screen_name = screenName,count=200)
    allTweets.extend(newTweets)
    
    oldestTweet = allTweets[-1].id - 1
    
    while len(newTweets) > 0:
        print("getting tweets before %s" % (oldestTweet))
        newTweets = api.user_timeline(screen_name = screenName, count = 200, max_id = oldestTweet)
        allTweets.extend(newTweets)
        oldestTweet = allTweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(allTweets)))
    
    #transform the tweepy tweets into a 2D array that will populate the database
    dataTweets = []
    for tweet in allTweets:
        dataTweets.append(getOriginalTime(tweet))
    insertTweetData(dataTweets)

def getOriginalTime(tweet):
    if(tweet.retweeted):
        originaltTweet = api.get_status(tweet.id_str)
        return [originaltTweet.id_str, str(originaltTweet.retweeted_status.created_at)]
    else:
        return [tweet.id_str, str(tweet.created_at)]

def insertTweetData(dataTweets):
    conn = sqlite3.connect('trumpgret.db')
    c = conn.cursor()

    for tweet in dataTweets:
        print("Inserted")
        c.execute("INSERT OR IGNORE INTO tweets VALUES (?,?)", tweet)
	
    conn.commit()
    conn.close()
    
def readDB():
    #current 2430
    conn = sqlite3.connect('trumpgret.db')
    c = conn.cursor()

    #c.execute("INSERT OR IGNORE INTO tweets VALUES (?,?)", tweet)
    c.execute('SELECT * FROM tweets')
    results = c.fetchall()
    print (len(results))
	
    #conn.commit()
    conn.close()
	
	
#getAllTweets("Trump_Regrets")
readDB()