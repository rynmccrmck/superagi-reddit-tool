import os
import praw

reddit = praw.Reddit(
    client_id=os.environ.get('REDDIT_CLIENT_ID'),  
    client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
    user_agent="todo-toronto:1.0.0 (by u/Able_Definition6250)",
)


for submission in reddit.subreddit("toronto").hot(limit=10):
    if submission.title.startswith("Things to do:"):
        break 

# TODO this could be passed to llm for safety (at a cost)
title = submission.title
entries = submission.selftext.split("\n")[2:]
titles = entries[::4]
urls = entries[2::4]
events = zip(titles, urls)

