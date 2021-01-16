import tweepy
from flask import Flask, render_template

app = Flask(__name__)

consumer_id = ""
consumer_key = ""
callback_uri = "oob"
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
auth = tweepy.OAuthHandler(consumer_id, consumer_key, callback_uri)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/tweets/')
def get_tweets():
    my_timeline = api.home_timeline()
    twitter_data = []
    col_header = set()
    allowed_types = [int, str]
    for status in my_timeline:
        status_dict = dict(vars(status))
        status_key = status_dict.keys()
        single_tweet_data = {"user": status.user.screen_name, "author": status.author.screen_name}
        for k in status_key:
            v_type = type(status_dict[k])
            if v_type in allowed_types:
                single_tweet_data[k] = status_dict[k]
                col_header.add(k)
        twitter_data.append(single_tweet_data)
    return render_template('tweets.html', tweets=twitter_data)


@app.route('/user/')
def username_tweets():
    me = api.me().screen_name
    return render_template('user.html', user=me)


if __name__ == '__main__':
    app.run()
