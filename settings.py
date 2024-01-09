from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str
    admin_id: int
    database_url_async: str

settings = Settings(_env_file='.env')
