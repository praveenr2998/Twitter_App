""" This file contains all the functions that are needed to perform DB related operations using Twitter API

FUNCTION NAME               -    WHAT THE FUNCTION DOES

insertDataToDb              -   Insert the tweets into Postgres DB.
get_tweets_from_twitter     -   Get tweets using twitter API
filter_tweets_by_date       -   Filter tweets from data fetched from twitter API
fetch_tweets_from_db        -   Fetch tweets from DB using user_name
filter_tweets_by_parameters -   Filter tweets fetched from DB based on keyword/date
fetch_user_ids              -   Get user IDs from DB.




"""

import psycopg2
import tweepy

from psycopg2 import Error
from datetime import datetime

from tweepy.models import Status
from psycopg2.extras import execute_batch

from query import FETCH_DATA_CHRONOLOGICALLY, \
    FETCH_USER_ID, INSERT_INTO_USER_ID_TABLE, FETCH_ALL_USER_ID,\
    BULK_INSERT_TWEETS_TO_DB    


class features():
    
    def __init__(self):
        try:
            self.connection = psycopg2.connect(user="praveen",
                                  password="29121998Pp@",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
            self.cursor = self.connection.cursor()
            
        except (Exception, Error) as error:
            return "Error while connecting to DB : " + str(error)




    def insertDataToDb(self, user_name):
        r'''This function is used to insert data into the database

            Calls Functions - get_tweets_from_twitter, filter_tweets_by_date

            It returns a dictionary having a message and status of the operation.

            Parameters
            ----------

            Below are the KeyWord Arguments that can be passed

            user_name   :    String - Twitter user name

            
            Raises
            ------
            An error response Json having details about the reason of failure
            
            
            Returns
            -------
            Dictionary(Message and Success Status : True)                          : On Sucess
            Dictionary(Message + Failure Reason and Success Status : False)        : On Failure

        '''


        try:
            tweets_from_twitter, status = self.get_tweets_from_twitter(user_name)
            if status is not True:
                return {"Message" : status,
                        "Status"  : "Failed"}


            self.cursor.execute(FETCH_USER_ID.format(user_name))
            fetch_result = self.cursor.fetchall()

            if len(fetch_result) != 0:
                bulk_update_list = []
                self.cursor.execute(FETCH_DATA_CHRONOLOGICALLY.format(user_name))                
                fetch_results = self.cursor.fetchall()
                for row in fetch_results:
                    start_date = row[2]
                    break
                
                
                tweet_object_list, status = self.filter_tweets_by_date(tweets_from_twitter, start_date, datetime.now())
                if status is not True:
                    return {"Message" : status,
                            "Status"  : "Failed"}

                               
                for tweet in tweet_object_list:
                    post_date = tweet.created_at
                    tweet_text = tweet.full_text
                    if tweet_text.startswith("RT"):
                        tweet_text = tweet.retweeted_status.full_text
                    tweet_text = tweet_text.replace("'","''")
                    bulk_update_list.append((user_name, tweet_text, post_date))

                execute_batch(self.cursor, BULK_INSERT_TWEETS_TO_DB, bulk_update_list)
                return {"Message" : "Latest Tweets Are Inserted into DB",
                        "Status"  : "Success"}


            
            else:
                bulk_update_list = []
                self.cursor.execute(INSERT_INTO_USER_ID_TABLE.format(user_name))
                for tweet in tweets_from_twitter:
                    post_date = tweet.created_at
                    post_date = str(post_date).replace(" ","T")
                    tweet_text = tweet.full_text
                    if tweet_text.startswith("RT"):
                        tweet_text = tweet.retweeted_status.full_text
                    tweet_text = tweet_text.replace("'","''")
                    bulk_update_list.append((user_name, tweet_text, post_date))
                execute_batch(self.cursor, BULK_INSERT_TWEETS_TO_DB, bulk_update_list)

            self.connection.commit()
#            self.connection.close()
#            self.cursor.close()
            return {"Message" : "Tweets Are Inserted into DB",
                    "Status"  : "Success"}



        except (Exception, psycopg2.Error) as error:
            return {"Message" : "Error While Inserting Tweets To DB - " + str(error),
                    "Status"  : "Failed"}








    def get_tweets_from_twitter(self, username):
        r'''This function is used to get tweets from twitter using Twitter API

            It returns tweets, status(True/error message).

            Parameters
            ----------

            Below are the KeyWord Arguments that can be passed

            username    :    String - Twitter username whose tweets need to be fetched.

            
            Raises
            ------
            None, Reason of failure
            
            
            Returns
            -------
            Tweets, Status(True)            : On Sucess
            None, Reason for failure        : On Failure

        '''
        
        consumer_key = "KzW1PNX6dIjzsy7Ha1aPBipYZ"
        consumer_secret = "VDhRJMq8j4F7QFpwKq6ML6PwKhCrF1ud6NjjqjJCbrlQEV3rAi"
        access_key = "1280193278470545409-mjmL6OInDBrMtjRWNuXjQFJ7ZItUmj"
        access_secret = "2DBIIEnO7KGK2dAGleoNVPCZD5DaPZJ22k5k6BVAqKVtK"

        
        
        try:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_key, access_secret)

            tweets = []
            api = tweepy.API(auth)
            # tweets = api.user_timeline(screen_name=username, count=1000)
            for status in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode="extended").items(500):
                tweets.append(status)

            return tweets, True
        
        except Exception as e:
            return None, "Error in fetching tweets using Twitter API : " + str(e)








    def filter_tweets_by_date(self, tweets_from_twitter, start_date, end_date):
        r'''This function is used to filter tweets by date so that tweets between the specified dates are returned

            It returns tweets

            Parameters
            ----------

            Below are the KeyWord Arguments that can be passed

            tweets_from_twitter    :    Object - Tweets fetched using twitter API.
            start_date             :    Date Format similar to one fetched by datetime library.
            end_date               :    Date Format similar to one fetched by datetime library.


            
            Raises
            ------
            None, Reason of failure
            
            
            Returns
            -------
            Tweets, Status(True)            : On Sucess
            None, Reason for failure        : On Failure

        '''

        try:
            tweet_object_list = []
            
            for tweet in tweets_from_twitter:
                tweet_date_str = str(tweet.created_at)
                split_tweet_date_str = tweet_date_str.split("+")
                tweet_date = datetime.strptime(split_tweet_date_str[0], '%Y-%m-%d %H:%M:%S')
                if tweet_date <= end_date and tweet_date > start_date:
                    tweet_object_list.append(tweet)

            return tweet_object_list, True

        except Exception as e:
            return None, e





    def fetch_tweets_from_db(self, user_name):
        r'''This function is used to fetch tweets from DB

            It returns tweets from DB, status(True/error message).

            Parameters
            ----------

            Below are the KeyWord Arguments that can be passed

            username    :    String - Twitter username whose tweets need to be fetched.

            
            Raises
            ------
            None, Reason of failure
            
            
            Returns
            -------
            Tweets, Status(True)            : On Sucess
            None, Reason for failure        : On Failure

        '''

        try:
            self.cursor.execute(FETCH_DATA_CHRONOLOGICALLY.format(user_name))
            fetch_result = self.cursor.fetchall()
            
            return fetch_result, True

        except Exception as e:  
            return None, "Error in fetching tweets from DB : " + str(e)





    def filter_tweets_by_parameters(self, data, keyword, from_date, to_date):
        r'''This function is used to filter tweets by keyword/dates.

            It returns tweets from DB, status(True/error message).

            Parameters
            ----------

            Below are the KeyWord Arguments that can be passed

            data      :    Tuple  - Tweets fetched from DB
            keyword   :    String - Word or sentence used to filter tweets
            from_date :    String - From date as a string
            to_date   :    String - To date as a string

            
            Raises
            ------
            None, Reason of failure
            
            
            Returns
            -------
            Tweets, Status(True) or empty list(when no match is found)          : On Sucess
            None, Reason for failure                                            : On Failure

        '''

        try:
            return_data = []
            if from_date != "" and to_date != "":
                from_date = from_date + " 00:00:00"
                from_date = datetime.strptime(from_date, "%d/%m/%Y %H:%M:%S")
                to_date = to_date + " 00:00:00"
                to_date = datetime.strptime(to_date, "%d/%m/%Y %H:%M:%S")


            if keyword != "" and from_date != "" and to_date != "":
                for _ in data:
                    if keyword.lower() in _[1].lower() and from_date <= _[2] <= to_date :
                        return_data.append(_)
                return return_data, True

            
            if keyword  == "" and from_date != "" and to_date != "":
                for _ in data:
                    if from_date <= _[2] <= to_date :
                        return_data.append(_)
                return return_data, True

            
            if keyword  != "" and from_date == "" and to_date == "":
                for _ in data:
                    if keyword.lower() in _[1].lower() :
                        return_data.append(_)
                return return_data, True





        except Exception as e:
            return None, "Error in filtering data from DB : " + str(e)






    
    def fetch_user_ids(self):
        r'''This function is used to fetch user ids from DB.

            It returns user ids and status(True/reason for failure).

            Parameters
            ----------

            No parameters are passed to this function
            
            Raises
            ------
            user_id list, Reason of failure
            
            
            Returns
            -------
            User id - List, True          : On Sucess
            
        '''

        
        try:
            self.cursor.execute(FETCH_ALL_USER_ID)
            fetch_result = self.cursor.fetchall()

            user_ids = []
            for data in fetch_result:
                user_ids.append(data[0])

            return user_ids, True

        except Exception as e:
            return user_ids, str(e)



