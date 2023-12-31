import praw
from praw.models import TimeFilter
from pydantic import BaseModel, Field
from typing import Type, Optional, List
from superagi.tools.base_tool import BaseTool

class RedditReadSchema(BaseModel):
    subreddit: str = Field(..., description="Subreddit to read from")
    sort: str = Field(..., description="Sorting method (hot, new, top, rising)")
    limit: Optional[int] = Field(10, description="Limit on number of submissions to fetch")

class RedditReadTool(BaseTool):
    """
    Reddit Read Tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    llm: Optional[BaseLlm] = None
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
        user_agent = self.get_tool_config("REDDIT_CLIENT_USERAGENT", "todo-app:1.0.0 (by u/youruser")

        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
    
        time_filter = TimeFilter.all
        if time_range == 'hour':
            time_filter = TimeFilter.hour
        elif time_range == 'day':
            time_filter = TimeFilter.day
        elif time_range == 'week':
            time_filter = TimeFilter.week
        elif time_range == 'month':
            time_filter = TimeFilter.month

        if subreddit:
            search_results = reddit.subreddit(subreddit).search(query, time_filter=time_filter)
        else:
            search_results = reddit.subreddit("all").search(query, time_filter=time_filter)

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
