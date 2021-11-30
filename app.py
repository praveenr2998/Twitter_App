from flask import Flask, request,render_template
from tweepy.models import Status
from models import features


app = Flask(__name__)

# To insert tweets to DB
@app.route('/')
def hello_world():
    global obj1
    obj1 = features()
    return obj1.insertDataToDb()


# Display tweets chronologically
@app.route('/fetchdata')
def main_fetch_tweets_from_db():
    data, message = obj1.fetch_tweets_from_db("Praveen18200450")
    
    if message is True:
        return render_template('chronological_tweet_display.html', data=data)
    
    else:
        return {"Message" : message,
                "Status"  : "Failed"}





if __name__ == '__main__':
	app.run()