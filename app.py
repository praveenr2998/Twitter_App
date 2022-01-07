from flask import Flask, request,render_template, Flask, url_for, flash, redirect, session
from tweepy.models import Status
from models import features
from forms import FilterForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

global obj1
obj1 = features()



# Login
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.user_name.data is not None:
            user_name = form.user_name.data
            session["user_name"] = user_name
            response = obj1.insertDataToDb(user_name)
            if response.get("Status") is not None:
                return redirect(url_for('fetchdataDB'))
        else:
            return "Unsuccessful Login"
    return render_template('login.html', title='Login', form=form)







# Fetch data from Db and display tweets chronologically
@app.route('/fetchdataDB')
def fetchdataDB():
    data, message = obj1.fetch_tweets_from_db(session.get("user_name"))
    
    if message is True:
        return render_template('chronological_tweet_display.html', data=data)
    
    else:
        return {"Message" : message,
                "Status"  : "Failed"}






# Filter dates by text, from date, to date
@app.route("/filter", methods=['GET', 'POST'])
def filter():
    form = FilterForm()
    if form.validate_on_submit():
        data, message = obj1.fetch_tweets_from_db(session.get("user_name"))
        if message is True:
            return_data, status = obj1.filter_tweets_by_parameters(data, form.text.data, form.from_date.data, form.to_date.data)
            if status is True:
                return render_template('chronological_tweet_display.html', data=return_data)
            else:
                return "Unsuccessful"
        
        
    return render_template('filter.html', title='Filter', form=form)







# Cron job to update with latest tweets
@app.route("/cronjob", methods=['GET'])
def cron_job():
    cron_flag = False
    user_ids, status = obj1.fetch_user_ids()
    if status is True and len(user_ids)>0:
        for ids in user_ids:
            cron_response = obj1.insertDataToDb(ids)
            print(cron_response.get("Message"))
            if cron_response.get("Status") == 'Success':
                cron_flag = True
            else:
                cron_flag = False
    
    else:
        return {"Status" : cron_flag,
                "Message" : "Cronjob Unsuccessful : Either no user_ids present in DB or " + str(status)}
    
    if cron_flag is True:
        return {"Status" : cron_flag,
                "Message" : "Cronjob successful"}
    else:
        return {"Status" : cron_flag,
                "Message" : "Cronjob Unsuccessful : " + str(cron_response.get("Message"))}
        




if __name__ == '__main__':
    app.run(host = '0.0.0.0')
