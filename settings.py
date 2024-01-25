from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Database:
    async_db_url: str
    sync_db_url: str
    db_echo: bool


@dataclass
class Settings:
    bots: Bots
    db: Database


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('BOT_TOKEN'),
            admin_id=env.int('ADMIN_ID')
        ),
        db=Database(
            async_db_url=env.str('DATABASE_URL_ASYNC'),
            sync_db_url=env.str('DATABASE_URL_SYNC'),
            db_echo=env.bool('DB_ECHO')
        )
    )


settings = get_settings('.env')