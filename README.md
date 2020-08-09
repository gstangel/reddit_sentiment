# reddit_sentiment
Reddit_Sentiment is a python based application that enables a user to calculate the sentiment of a subreddit seamlessly

Prerequisites:
    Python 3 installed locally
    TextBlob module- docs and install procedure can be found here https://textblob.readthedocs.io/en/dev/
    A reddit account
    A bot registered with reddit. Once logged in, you can sign up for a developer app at this link https://www.reddit.com/prefs/apps
    
Once registered with reddit for a bot, insert your credentials into the credentials.py file in their respective places.
This app utilizes a previously developed easy_reddit_to_json to pull raw data from reddit and organize it into a json file

Relevant variables to manipulate include the targetSubreddit variable.  You can type any subreddit into this field just as it appears on reddit.  This will be the subreddit that will be scraped

The postLimit variable limits how many posts are scraped from the subreddit.  Value can be from 1-200

Here is a flowchart of how the script is setup



    
