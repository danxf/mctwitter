from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import time as time_module
import calendar
import os
import sys
import numpy
from time import time
import json
import _pickle as pkl
import numpy as np
from time import localtime, strftime
import sys
import datetime
import re

MAX_COUNT = 200

def get_time_str():
    return str(datetime.datetime.now())


def read_keys(idx):
    with open('cred.crd','rb') as f:
        u = json.load(f)    
    
    return u[idx]['ck'],u[idx]['cs'],u[idx]['at'],u[idx]['ats']

def remove_links_from_tweet(text):
    return re.sub(r'https?:\/\/.*[\r\n]*','',text)

def read_user_file():
    
    with open('user_list.txt','r') as f: 
        usernames = f.read().splitlines() 
    return usernames

if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception('Pass API credentials index as parameter')
    
    #reading Twitter API credentials from file
    consumer_key,consumer_secret, access_token, access_token_secret = read_keys(sys.argv[1]) 
    
    #Authenticating with Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    #Creating API object for timeline requests
    api = tweepy.API(auth, wait_on_rate_limit=True, parser=tweepy.parsers.JSONParser())
    
    api_call_counter = 0
    start_time = time_module.time()
    
    #Reading user names from file
    user_names = read_user_file()
    
    timeline = []
    for username in user_names: 
        userid = api.get_user(username)['id']
        
        print('Processing user:' + username + ' ' + str(userid))    
        
        #Getting the time line of userid
        #First API call is sperate since we do no know the max_id parameter
        try:
            api_call_counter+=1
            partial_timeline = api.user_timeline(userid, count=MAX_COUNT, tweet_mode="extended")
            print ('collected {} tweets'.format(len(partial_timeline)))
        except Exception as e:
            print('Exception at first api call!' + get_time_str())                
            print (repr(e))
            print('moving to next user')
            continue
        
        if (len(partial_timeline) == 0): #user has no tweets
            print ('this user has no tweets at all')
            continue


        maxid = partial_timeline[-1]['id'] 
        timeline += partial_timeline
        
        
        while(True):
            #Rate limit handling
            if(api_call_counter >= 890):
                print('rate limit reached, sleeping  ....')
                cur_time = time_module.time()
                dif = cur_time-start_time
                
                if(dif >= 60*15):
                    print ('no need to sleep')
                else:
                    print ('sleeping for' + str(60*15-dif) + ' minutes')
                    time_module.sleep(60*15-dif)
                    print('done sleeping')
                    start_time=cur_time
                api_call_counter = 0
                
                
            print ('.',)
            sys.stdout.flush()
            
            try:
                api_call_counter+=1
                partial_timeline = api.user_timeline(userid, count=MAX_COUNT, max_id=maxid-1,tweet_mode="extended")
                print ('collected {} tweets'.format(len(partial_timeline)))
            except Exception as e:
                print('Exception in inner collect loop' + get_time_str())
                print(repr(e))
                break
            
            if(len(partial_timeline) == 0): #done with timeline
                break
            
            maxid = partial_timeline[-1]['id']
            print('maxid : {}'.format(maxid))
            timeline += partial_timeline
        
    #Tokenizing, removing links and filterting tweets    
        
    non_replies = []
    self_replies = []
    replies = []
    all_non_replies = []


    for tweet in timeline:
        #tweets come in dictionary format, extracting just the text
        tweet_text = tweet['full_text']
        #ignoring retweets (retweets are always preceeded by "RT" in the tweet's text)
        if tweet_text[:2] == 'RT': 
            continue
        #non-reply tweets
        if  tweet['in_reply_to_screen_name'] is None: 
            non_replies.append(remove_links_from_tweet(tweet_text))
            all_non_replies.append(remove_links_from_tweet(tweet_text))
        #self replies (for long text spanning across multiple tweets)
        elif tweet['in_reply_to_screen_name'] in user_names: 
            self_replies.append(remove_links_from_tweet(tweet_text))
            all_non_replies.append(remove_links_from_tweet(tweet_text))
        #replies no non relevant users go in sperate list
        else: 
            replies.append(remove_links_from_tweet(tweet_text))
    
    #White space regex tokenization
    tokenized = [list(filter(lambda s: len(s)>0, re.split(r'[\s]', text))) for text in all_non_replies] 
    
    #Saving tweets
    f=open('parsed_tweets.pkl', 'wb')
    pkl.dump(tokenized, f)
    f.close()
    
