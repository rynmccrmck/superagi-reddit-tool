import os
import re
import praw

URL_PATTERN = r'https.*\b'
def extract_url(text):
    return re.findall(URL_PATTERN, text)[-1]

reddit = praw.Reddit(
    client_id=os.environ.get('REDDIT_CLIENT_ID'),  
    client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
    user_agent="todo-toronto:1.0.0 (by u/Able_Definition6250)",
)

matched = None
subreddit = reddit.subreddit("toronto")
for submission in subreddit.search("Things to do", sort="new", time_filter="week"):
    if submission.title.lower().startswith("things to do"):
        matched = submission
        break
    

# TODO this could be passed to llm for safety (at a cost)
if matched:
    title = matched.title
    entries = matched.selftext.split("\n")[2:]
    titles = entries[::4]
    urls = entries[2::4]
    events = zip(titles, urls)

    json_results = []
    for name,url in events:
        print(f"{name} - {url}")
        url_fixed = extract_url(url)
        json_results.append({'name': name, 'url': url_fixed})
    print(json_results)
