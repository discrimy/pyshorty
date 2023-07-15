from pydantic import RedisDsn
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    REDIS_URL: RedisDsn


app_settings = AppSettings(_env_file=".env")
