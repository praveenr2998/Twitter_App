INSERT_TWEETS_TO_DB = '''
INSERT INTO twitterdata (user_id,tweet,post_date)
VALUES ('{}', '{}', '{}');
'''

FETCH_DATA_CHRONOLOGICALLY = '''
SELECT user_id, tweet, post_date
FROM twitterdata where user_id = '{}'
ORDER BY post_date desc;
'''

FETCH_USER_ID = '''
SELECT user_id from userid where user_id = '{}'; 
'''

INSERT_INTO_USER_ID_TABLE = '''
INSERT INTO userid (user_id)
VALUES ('{}');
'''


FETCH_ALL_USER_ID = '''
SELECT user_id from userid ;
'''