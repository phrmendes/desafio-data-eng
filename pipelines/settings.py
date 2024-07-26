from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the pipelines."""

    BASE_URL: str = Field(default=...)
