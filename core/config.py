import os
from pydantic_settings import BaseSettings
# import boto3
# from ..services.s3.private_bucket.private_bucket import PrivateBucket

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()