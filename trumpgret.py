import tweepy
import sqlite3
import os
import requests
import json
import time
from bs4 import BeautifulSoup

jsonFile = open("twitter_data.json", "r")
data = json.load(jsonFile)
jsonFile.close()

#Twitter account keys
consumerKey = data["consumer_key"]
consumerSecret = data["consumer_secret"]
accessToken = data["access_token"]
accessTokenSecret = data["access_token_secret"]

#setting up tweepy api
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth) 

def getAllRetweets(screenName):
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
        try:
            if(tweet.retweeted_status):
                dataTweets.append(getOriginalTime(tweet))
        except AttributeError:
            pass
    print("Found: %s retweets" % len(dataTweets))
    insertTweetData(dataTweets)

def getMostRecentRetweets(screenName, count):
    allTweets = []
    
    newTweets = api.user_timeline(screen_name = screenName,count=count)
    allTweets.extend(newTweets)
    
    dataTweets = []
    for tweet in allTweets:
        try:
            if(tweet.retweeted_status):
                dataTweets.append(getOriginalTime(tweet))
        except AttributeError:
            pass
    print("Found: %s retweets" % len(dataTweets))
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
        c.execute("INSERT OR IGNORE INTO tweets VALUES (?,?)", tweet)
	
    conn.commit()
    conn.close()

def getDBTweets():
    conn = sqlite3.connect('trumpgret.db')
    c = conn.cursor()

    c.execute('SELECT * FROM tweets')
    results = c.fetchall()
    print (len(results))
	
    conn.close()
    return results
    
def getMostRecentTweetDB():
    conn = sqlite3.connect('trumpgret.db')
    c = conn.cursor()

    c.execute('SELECT * FROM tweets ORDER BY id DESC LIMIT 1')
    result = c.fetchone()
    print (result[0])
	
    conn.close()

def initDB():
    if not ([s for s in os.listdir(os.getcwd()) if ".db" in s]):
        con = sqlite3.connect('trumpgret.db')
        cursor = con.cursor()
        
        # Create table
        cursor.execute('''CREATE TABLE IF NOT EXISTS tweets
                     (id integer primary key, date text)''')
        con.close()
        
def readTotalTweetValue():
    page = requests.get("https://twitter.com/Trump_Regrets")
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.find_all(class_='ProfileNav-value')[0].text.replace(',', '')

def updateTweetDB():
    jsonFile = open("twitter_data.json", "r")
    data = json.load(jsonFile)
    jsonFile.close()
    newTweetsNumber = int(readTotalTweetValue()) - int(data["total_tweets"])
    if(newTweetsNumber > 0):
        getMostRecentRetweets("Trump_Regrets", newTweetsNumber)
        #Changing total_tweets and last_update in json
        data["total_tweets"] = int(readTotalTweetValue())
        data["last_update"] = time.strftime("%Y-%m-%d")
    
        jsonFile = open("twitter_data.json", "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()
        return "Saved %s tweets to database" % newTweetsNumber
    else:
        return "No new tweets"

#getAllRetweets("placeholderYael")
#getAllRetweets("Trump_Regrets")

initDB()
#readTotalTweetValue()
#updateTweetDB()