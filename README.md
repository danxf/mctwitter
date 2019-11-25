# mctwitter
This is a text generator based on Markov chains. It learns from twitter data and can be used to mimic existing writing patterns of people.

## Requirements:
* NumPy
* [Tweepy API](http://docs.tweepy.org/en/v3.5.0/index.html)

## Usage:
* First time use:
    * Enter the user names whose timelines will be collected (this is what follows the '@' at Twitter) into `user_list.txt` (one per line). The tweets will be used to build a dictionary of words that will be used for generation. The usenames can share common talking subjects or be completely different. This data will determine the models' output. 
    * Edit the `cred.crd` file with `consumer_key`, `consumer_secret`, `access_token` and `access_token_secret` that you recieved from Twitter. The file has place for mutiple accounts. If you only have one just enter it as number 1 and leave the rest empty.
    * Run `collect_tweets.py` and pass the account number as a parameter.
* Generation:
    * Run `generate_text.py` and pass how many tweets to generate as a parameter. Output will be printed to `gen_output.txt`.
