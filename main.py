import praw
import os.path
import json
import glob
from textblob import TextBlob
from statistics import mean
import credentials

#client id, secret key, bot name, and username read from credentials.py
reddit = praw.Reddit(client_id = credentials.clientID,
                    client_secret = credentials.clientSecret,
                    user_agent = credentials.userAgent, 
                    username = credentials.userName)


target_subreddit = 'depression'#the subreddit to be queried
post_limit = 2000 #limit the posts to be obtained, every 100 added results in a 2 second request delay


def get_data():
    titles = [] #list of all the text in post titles
    bodys = [] #list of all the body text
    comments = [] #list of all of the comment text

    """
    this iterates though the API call, .hot indicates what sorting method the call should use.  
    You have the options to sort by .new, .top, .controversial
    """
    for submission in reddit.subreddit(target_subreddit).hot(limit=post_limit): 
        try:
            titles.append(str(submission.title)) #add title of current post
            bodys.append(str(submission.selftext))#add body of current post

            for comment in submission.comments.list():#iterate though comments from request
                    if not ("bot" in comment.body):#filter out bots
                            #write comment to file
                        comments.append(comment.body)

        except AttributeError: #catch if there is no more comments
            continue
    print("request completed")#let user know request is done

    return titles,bodys,comments #return data lists

             

def clean_data(data):
    unwanted_chars = [",", "’", "!", "/n" "'", "."] #charecters to be removed
    titles, bodys, comments = [], [], [] #updated lists with removed comments

    for title in data[0]:
        for char in unwanted_chars: #loop through titles, remove unwanted charecters
            title.replace(char, " ")
        titles.append(title)

    for body in data[1]:
        for char in unwanted_chars: #loop through bodys, remove unwanted charecters
            body.replace(char, " ")
        bodys.append(body)

    for comment in data[2]:#loop through comments, remove unwanted charecters
        for char in unwanted_chars:
            comment.replace(char, " ")
        comments.append(comment)

    print("unwanted charecters removed")#let user know request is done

    return titles,bodys,comments #return new clean lists


#this function gets overall sentiement for the data
def get_sentiment(data):
    polarity = [] #an array of numbers in range (-1,1), where -1 is very negative, 0 is neutral, 1 is postitve
    subjectivity = [] #an array of numbers in range (-1,1), where -1 is very subjective, 0 is neutral, 1 is not subjective

    for title in data[0]:
        polarity.append(TextBlob(title).sentiment.polarity) #append polarity using textblob
        subjectivity.append(TextBlob(title).sentiment.subjectivity) #append subjectivity using textblob

    for body in data[1]:
        polarity.append(TextBlob(body).sentiment.polarity)#append polarity using textblob
        subjectivity.append(TextBlob(body).sentiment.subjectivity)#append subjectivity using textblob
    
    for comment in data[2]:
        polarity.append(TextBlob(comment).sentiment.polarity)#append polarity using textblob
        subjectivity.append(TextBlob(comment).sentiment.subjectivity)#append subjectivity using textblob

    print("sentiment found")

    return polarity, subjectivity #return both arrays


#this function determines the result of the TextBlob NLP, and outputs to the user in a friendly format
def get_result(sentiment):
    negative_count = 0 #number of negative posts
    positive_count = 0 #number of positive posts

    for polarity in sentiment[0]:
        if(polarity > 0):
            positive_count += 1 #increment positive count
        else:
            negative_count += 1 #increment negative count
    
    if(negative_count > positive_count):
        print("Overall, " + target_subreddit + " is on average negative.  "  +
         "This query produced " + str(negative_count) + " negative posts, and " + str(positive_count) + " positive posts.") #print result
    else:
        print("Overall, the subreddit " + target_subreddit + " is on average positive.  "  +
         "This query produced " + str(positive_count) + " negative posts, and " + str(negative_count) + " negative posts.") #print result


if __name__ == '__main__':
    data = get_data() #get initial data from subreddit
    cleaned_data = clean_data(data) # call get_data function, which also calls the clean_data function
    sentiment = get_sentiment(cleaned_data) #create a list of predicted sentiment for each comment/post/title
    get_result(sentiment) #determine the average sentiment of the entire query, and display in a friendly format
    
