from abc import ABC
from superagi.tools.base_tool import BaseToolkit, BaseTool, ToolConfiguration
from typing import Type, List
from reddit_read_tool import RedditReadTool
from reddit_write_tool import RedditWriteTool
from superagi.types.key_type import ToolConfigKeyType

class TwitterToolkit(BaseToolkit, ABC):
    name: str = "Reddit Toolkit"
    description: str = "Reddit Tool kit contains all tools related to Reddit"

    def get_tools(self) -> List[BaseTool]:
        return [RedditReadTool(), RedditWriteTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return [
            ToolConfiguration(key="REDDIT_CLIENT_ID", key_type=ToolConfigKeyType.STRING, is_required= True, is_secret = True),
            ToolConfiguration(key="REDDIT_CLIENT_SECRET", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret= True),
            ToolConfiguration(key="REDDIT_CLIENT_USERAGENT", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret= FALSE)
        ]