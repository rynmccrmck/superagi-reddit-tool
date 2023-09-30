import praw
from pydantic import BaseModel, Field
from typing import Any, Type, Optional, List
from superagi.tools.base_tool import BaseTool

class RedditReadSchema(BaseModel):
    subreddit: str = Field(..., description="Subreddit to read from")
    query: str = Field(..., description="Search term to query")
    time_range: Optional[str] = Field(..., description="The time range to search in (possible values: hour, day, week, month, year, all)")
    limit: Optional[int] = Field(10, description="Limit on number of submissions to fetch")

class RedditReadTool(BaseTool):
    """
    Reddit Read Tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    llm: Optional[Any] = None
    name = "RedditRead"
    description = (
        "A tool for performing a Reddit search and extracting submissions and comments."
        "Input should be a subreddit."
    )
    name = "Reddit Read Tool"
    description = (
        "A tool for reading submissions from a specified subreddit"
    )
    args_schema: Type[RedditReadSchema] = RedditReadSchema

    class Config:
        arbitrary_types_allowed = True
    
    def _execute(self, query: str, subreddit: Optional[str] = None, time_range: Optional[str] = None, limit: Optional[int]= 1) -> List[dict]:
        """
        Execute the RedditRead search tool.

        Args:
            query : The query to search for.
            subreddit : The subreddit to search in.
            time_range : The time range to search in (possible values: hour, day, week, month, year, all)
            limit : The limit on number of submissions to fetch.

        Returns:
            Search result summary along with related links
        """
        client_id = self.get_tool_config("REDDIT_CLIENT_ID")
        client_secret = self.get_tool_config("REDDIT_CLIENT_SECRET")
        user_agent = self.get_tool_config("REDDIT_CLIENT_USERAGENT")
        if not user_agent:
            user_agent = "todo-app:1.0.0 (by u/youruser)"

        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
        if not time_range:
            time_range = 'all'

        if subreddit:
            search_results = reddit.subreddit(subreddit).search(query, time_filter=time_range, limit=limit)
        else:
            search_results = reddit.subreddit("all").search(query, time_filter=time_range, limit=limit)

        submission_data = []
        for submission in search_results:
            submission_data.append({
                'title': submission.title,
                'author': str(submission.author),
                'url': submission.url,
                'score': submission.score,
                'self_text': submission.selftext,
                'comments': submission.num_comments
            })
        return "\n".join(submission_data)
