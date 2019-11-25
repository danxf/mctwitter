
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _pickle as pkl
import numpy as np
import sys

def generate(markov_dict, start_words, max_length = 200, max_sentences = 3):
    generated_tweet = []
    cnt = 0
    #Choosing random start word
    curr_word = np.random.choice(start_words)
    generated_tweet.append(curr_word)
    cnt +=1
    Nsentences = 0
    while cnt<max_length:
        try:
            #Trying to continue from last word
            curr_word = np.random.choice(markov_dict[generated_tweet[cnt-1]])
        except KeyError:
            #If we cant (usually means end of the sentence) we start from one of the start words
            curr_word = np.random.choice(start_words)
        generated_tweet.append(curr_word)
        cnt += 1
        if curr_word[-1] == '.':
            Nsentences += 1
        
        if Nsentences == max_sentences:
            break
    
    #returns list of tokens
    return generated_tweet
                                                 
def build_dict():
    with open('parsed_tweets.pkl','rb') as f:
        text = pkl.load(f)
    
    #Building the dictionary
    markov_dict = dict()
    start_words = []
    for tweet in text:
        
        if len(tweet)>0: #sanity check (0 length tweets can result from tweets containing only links or heavy pre-processing)
            z = tweet
            if len(z) < 2: #ignoring short tweets
                continue
            start_words.append(z[0]) #seperate list for start words
            for i in range(1, len(z)):
                if z[i-1] in markov_dict:
                    markov_dict[z[i-1]].append(z[i])
                else:
                    markov_dict[z[i-1]] = [z[i]]
    return (markov_dict, start_words)

if __name__ == "__main__":
    if len(sys.argv) < 1:
        raise Exception('Specify how many tweets to generate')
    try:
        Ntweets_to_generate = int(sys.argv[1])
    except ValueError:
        raise Exception('Pass a number')
    
    (markov_dict, start_words) = build_dict()
                    
    #Writing output to file
    with open('gen_output.txt','a') as f:
        f.write('Generator Output:\n\n')
    for i in range(Ntweets_to_generate):
        with open('gen_output.txt','a') as f:
            #joining the list of tokens returned from the genrator and writing to file
            f.write(' '.join(generate(markov_dict, start_words))+'\n\n')
        
        
    
