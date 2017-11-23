from flask import Flask, jsonify
import os
from trumpgret import *

app = Flask(__name__)
#needed to see server refresh instantly while modyfing.
#app.debug = True

@app.route("/")
def main():
    return "Trumpgret backend running"
    
#REST route that returns all collected tweets in the DB
@app.route('/tweets', methods=['GET'])
def get_tweets():
    return jsonify(getDBTweets())

#REST route that updates DB with Trump_Regrets account's latest tweets 
@app.route('/update', methods=['GET'])
def update_tweets():
    return updateTweetDB()
    
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))