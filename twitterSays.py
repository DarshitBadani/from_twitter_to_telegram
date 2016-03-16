import os, time
import twython as Twython
from urllib import quote

## Twitter application authentication ##
# The following strings are placeholders, with dummy keys that will not work!
# Replace these keys, with your own. http://dev.twitter.com/docs/api/1.1/overview/. 
APP_KEY = 'XXXxxXXXxXxxXXXXxXxxxXxxXxXXxxXxXxXxXXXxX'
APP_SECRET = 'xxxXXxXXxXxXxxxXXxXxXxxXXXXxxXxXXXxxXXxxXxxxxxX'
OAUTH_TOKEN = 'XXxXXxXXxxXXxxXxXxxxXXXxXxxxXxXXXxxXxXxXxxXxxx'
OAUTH_TOKEN_SECRET = 'xXXxXXXxXxxXXXxXxxXxXXxXXXxXxXXXXxXxXXxXX'

api = Twython.Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
latest_tweet_id = 0

## Your Telegram Channel Name ##
channel_name = 'geremysays'
## Telegram Access Token ##
telegram_token = 'nnnnnnnnnnnnn:XxxXXXxXxXxXxXXxXxxXxxxxXx'
## Twitter User Name to get Timeline ##
user_name = 'GeremySays'

def first_run():
    file_exists = os.path.exists(channel_name+"_latest_id.txt")
    if file_exists is False:
        user_timeline = api.get_user_timeline(screen_name=user_name, count=2)
        tweet_id = user_timeline[1]['id']
        writeToLog(tweet_id)
def get_timeline(latest_tweet_id):
    user_timeline = api.get_user_timeline(screen_name=user_name, since_id=latest_tweet_id)
    return user_timeline
def writeToLog(msg):
    log_file = open(channel_name+"_latest_id.txt", "w")
    log_file.write(str(msg))
    log_file.close()
def read_latest_id():
    file_exists = os.path.exists(channel_name+"_latest_id.txt")
    if file_exists is False:
        writeToLog('0')
    else:
        log_file = open(channel_name+"_latest_id.txt", "r")
        line = log_file.read()
        log_file.close()
        if len(str(line)) < 2:
            return 0
        else:
            return line
def send_message(msg):
    msg = quote(msg, safe='')
    link = 'https://api.telegram.org/bot'+telegram_token+'/sendMessage?chat_id=@'+channel_name+'\&text="' + msg + '"'
    os.system('curl '+ link)
    
def main():
    latest_tweet_id = read_latest_id()
    user_timeline = get_timeline(latest_tweet_id)
    number_of_tweets = len(user_timeline)
    if number_of_tweets > 0:
        for i in reversed(range(0,number_of_tweets)):
            if user_timeline[i]['text']:
                print user_timeline[i]['text']
                send_message(user_timeline[i]['text'])
                time.sleep(4)
        latest_tweet_id = user_timeline[0]['id']
    writeToLog(latest_tweet_id)

first_run()
main()
