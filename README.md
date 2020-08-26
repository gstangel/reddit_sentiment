# Reddit_sentiment

Reddit_Sentiment is a python based application that enables a user to calculate the emotional sentiment of a subreddit 

Needed:
    
    -A reddit account
    
    -A bot registered with reddit. Once logged in, you can sign up for a developer app at this link https://www.reddit.com/prefs/apps
    
    -The requirements, which can be installed by running *pip install -r requirements.txt*
    
Once registered with reddit for a bot, insert your credentials into the *credentials.py* file in their respective places.

Relevant variables to manipulate include the targetSubreddit variable.  You can type any subreddit into this field just as it appears on reddit.  This will be the subreddit that will be scraped

The postLimit variable limits how many posts are scraped from the subreddit.  Be weary of pulling too much information at once, for every additional 100 posts, a 2 second delay is added.

The result will be displayed in the console when the script has finihsed running.

Here is a sample of what it will look like

*Overall, depression is on average negative.  This query produced 2916 negative posts, and 2542 positive posts.*





    
