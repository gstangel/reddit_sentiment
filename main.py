import praw
import os.path
import json
import glob
from textblob import TextBlob
from statistics import mean
import credentials

#insert your client id, secret key, bot name, and username 
reddit = praw.Reddit(client_id = credentials.clientID, client_secret = credentials.clientSecret, user_agent = credentials.userAgent, username = credentials.userName)

#Change what data you want appended to the JSON file using these variables
#Change what data you want appended to the JSON file using these variables
appendComments = True
appendAuthor = True
appendPostBody = True
appendTitle = True
appendDateTime = True
appendPostID = True
appendNumComments = True
appendNumUpvotes = True
appendFlair = True
appendUpvoteRatio = True
appendURL = True

targetSubreddit = "programming"
postLimit = 5


def post_to_json():
    #get current working directory
    cwd = os.getcwd()
    #make new folder from targetSubreddit variable
    targetFolder = os.path.join(cwd, targetSubreddit)
    #check if the folder was already created
    if os.path.isdir(targetFolder) == False:
        print("target folder made")
        #make new directory
        os.mkdir(targetFolder)
    #check if CWD is set correctly
    if (cwd != targetFolder):
        print("current working directory updated")
        os.chdir(targetFolder)
    #.new defines the sorting method, other methods include .hot, .top
    for submission in reddit.subreddit(targetSubreddit).hot(limit=postLimit):
        post = {}
        post['post'] = []
        post['comments'] = []
        
        try:
            #naming file as postid
            filename = str(submission.id) + ".json"
            if appendPostID == True:
                post['post'].append({'postID': str(submission.id)})
            if appendFlair == True:
                post['post'].append({'flair': str(submission.link_flair_text)})
            if appendNumUpvotes == True:
                post['post'].append({'upvotes': str(submission.score)})
            if appendUpvoteRatio == True:
                post['post'].append({'upvoteRatio': str(submission.upvote_ratio)})
            if appendAuthor == True:
                post['post'].append({'author': str(submission.author)})
            if appendTitle == True:
                post['post'].append({'title': str(submission.title)})
            if appendPostBody == True:
                post['post'].append({'bodytext': str(submission.selftext)})
            if appendDateTime == True:
                post['post'].append({'dateTimePosted': str(submission.created)})
            if appendURL == True:
                post['post'].append({'url': str(submission.url)})
                #adding comments  to dictionary
            if appendComments == True:
                commentCount = 1
                for comment in submission.comments.list():
                    
                    index = "comment" + str(commentCount)
                    
                        #filter out bots
                    if ("bot" in comment.body) == False:
                            #write comment to file
                        post['comments'].append({index: comment.body})
                        commentCount = commentCount + 1
            
            #writing JSON
            with open(filename, "w+") as outfile:
                json.dump(post, outfile)
                print(filename + " created")
            
     #catch encoding errors for emojis, no commetns
        except Exception as e:
            continue
    return targetFolder

def getSentiment(targetFolder):
    polarityArray = []
    subjectivityArray = []
    #iterate through files in target folder
    for filename in glob.glob(os.path.join(targetFolder, '*.json')):
        #while current file is open
        with open(filename, encoding='utf-8', mode='r') as currentFile:
            #replace new line charecters with blank
            data=currentFile.read().replace('\n', '')
            #get the polarity and subjectivity of the title
            polarityArray.append(TextBlob(json.loads(data)["post"][5]['title']).sentiment.polarity)
            subjectivityArray.append(TextBlob(json.loads(data)["post"][5]['title']).sentiment.subjectivity)
            
            #get the polarity and subjectivity of the body
            polarityArray.append(TextBlob(json.loads(data)["post"][6]['bodytext']).sentiment.polarity)
            subjectivityArray.append(TextBlob(json.loads(data)["post"][6]['bodytext']).sentiment.subjectivity)

            #keep track of commment index
            commentIndex = 0
            #while there is still comments left, 
            while(commentIndex < len(json.loads(data)["comments"])):
                
                currentComment = json.loads(data)["comments"][commentIndex]["comment" + str(commentIndex +1)]
                #add the polarity of the comment to the polarity array
                polarityArray.append(TextBlob(currentComment).sentiment.polarity)
                #add the polarity of the comment to the subjectivity array
                subjectivityArray.append(TextBlob(currentComment).sentiment.subjectivity)
                commentIndex = commentIndex + 1
    print("mean polarity of subreddit: " + str(mean(polarityArray)))
    print("mean subjectivity of subreddit: " + str(mean(subjectivityArray)))
            
if __name__ == '__main__':
    getSentiment(post_to_json())