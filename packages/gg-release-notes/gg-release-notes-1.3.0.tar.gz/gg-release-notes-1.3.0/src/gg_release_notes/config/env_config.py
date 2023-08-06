from typing import Optional

import pydantic


class EnvConfig(pydantic.BaseSettings):
    """Environment variables used in this project"""

    OPENAI_API_KEY: Optional[str]
    OPENAI_API_ORG: Optional[str]
    ENV_GITHUB_API_TOKEN: str
    SLACK_TOKEN: Optional[str]
    SLACK_CHANNEL_ID: Optional[str]
