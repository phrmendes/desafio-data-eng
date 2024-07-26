from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the pipelines."""

    BASE_URL: str = Field(default=...)
    CSV_FOLDER: str = Field(default=...)
    DB_CONNECTION_STRING: SecretStr = Field(default=...)
    DB_NAME: str = Field(default=...)
