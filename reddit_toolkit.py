from abc import ABC
from superagi.tools.base_tool import BaseToolkit, BaseTool, ToolConfiguration
from typing import List
from reddit_read_tool import RedditReadTool
from reddit_write_tool import RedditWriteTool

class TwitterToolkit(BaseToolkit, ABC):
    name: str = "Reddit Toolkit"
    description: str = "Reddit Tool kit contains all tools related to Reddit"

    def get_tools(self) -> List[BaseTool]:
        return [RedditReadTool(), RedditWriteTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_CLIENT_USERAGENT"]
