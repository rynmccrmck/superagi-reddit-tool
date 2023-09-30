import praw
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional

class RedditWriteSchema(BaseModel):
    title: str = Field(..., description="Title of the post")
    body: Optional[str] = Field(None, description="Body text of the post (optional)")
    url: Optional[str] = Field(None, description="URL of the post (optional)")
    subreddit: str = Field(..., description="Subreddit to post to")

class RedditWriteTool(BaseTool):
    name = "Reddit Tool"
    description = (
        "A tool for posting an AI generated text or link on Reddit"
    )
    args_schema: Type[RedditWriteSchema] = RedditWriteSchema

    class Config:
        arbitrary_types_allowed = True
    
    def _execute(self, title: str, body: Optional[str], url: Optional[str], subreddit: str) -> str:

        client_id = self.get_tool_config("REDDIT_CLIENT_ID")
        client_secret = self.get_tool_config("REDDIT_CLIENT_SECRET")
        user_agent = self.get_tool_config("REDDIT_CLIENT_USERAGENT", "todo-app:1.0.0 (by u/youruser")

        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
        
        sub = reddit.subreddit(subreddit)
        
        if url:
            post = sub.submit(title, url=url)
        else:
            post = sub.submit(title, selftext=body)
        
        return f"Post submitted successfully with ID: {post.id}"
