# Saama-Twitter_App
This web application fetches tweets from twitter using twitter api and facilitates easy viewing and filtering of tweets.
├── app.py
├── cronjob.py
├── cronjob.sh
├── forms.py
├── models.py
├── query.py
├── README.md
├── requirements.txt
├── static
│   └── main.css
└── templates
    ├── chronological_tweet_display.html
    ├── filter.html
    ├── layout.html
    └── login.html



# URLs
http://localhost:5000/   -   Login Page

http://localhost:5000/fetchdataDB - Display all tweets

http://localhost:5000/filter - Filter by keyword or dates or both

http://localhost:5000/cronjob - Update tweets(cronjob)


# Application demo video
https://user-images.githubusercontent.com/51623786/148258924-ea60d831-3bbf-4b14-862d-afc89901ca54.mp4


# Cron tab
![crontab](https://user-images.githubusercontent.com/51623786/148259733-c7acd960-7c67-4e65-86b2-befa81cc3220.png)


# Documentation
https://docs.google.com/document/d/1iwovHEttHeYSCK6J8_etPTme2FZEQVvCNYyUR04ZEqk/edit?usp=sharing
