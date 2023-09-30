import praw
from pydantic import BaseModel, Field
from typing import Type, Optional, List
from superagi.tools.base_tool import BaseTool

class RedditReadSchema(BaseModel):
    subreddit: str = Field(..., description="Subreddit to read from")
    sort: str = Field(..., description="Sorting method (hot, new, top, rising)")
    limit: Optional[int] = Field(10, description="Limit on number of submissions to fetch")

class RedditReadTool(BaseTool):
    name = "Reddit Read Tool"
    description = (
        "A tool for reading submissions from a specified subreddit"
    )
    args_schema: Type[RedditReadSchema] = RedditReadSchema

    class Config:
        arbitrary_types_allowed = True
    
    def _execute(self, subreddit: str, sort: str, limit: Optional[int]) -> List[dict]:
        client_id = self.get_tool_config("REDDIT_CLIENT_ID")
        client_secret = self.get_tool_config("REDDIT_CLIENT_SECRET")
        user_agent = self.get_tool_config("REDDIT_CLIENT_USERAGENT", "todo-app:1.0.0 (by u/youruser")

        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
        sub = reddit.subreddit(subreddit)
        
        if sort == 'hot':
            submissions = sub.hot(limit=limit)
        elif sort == 'new':
            submissions = sub.new(limit=limit)
        elif sort == 'top':
            submissions = sub.top(limit=limit)
        elif sort == 'rising':
            submissions = sub.rising(limit=limit)
        else:
            raise ValueError(f'Invalid sort method: {sort}')
        
        submission_data = []
        for submission in submissions:
            submission_data.append({
                'title': submission.title,
                'author': str(submission.author),
                'url': submission.url,
                'score': submission.score,
                'comments': submission.num_comments
            })
        
        return submission_data
