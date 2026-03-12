from dataclasses import dataclass
from environs import Env


@dataclass
class Database:
    db_name: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    owner_id: int


@dataclass
class Config:
    bot: TgBot
    db: Database

def load_config(path):
    env: Env = Env()

    env.read_env(path)

    return Config(
        bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            owner_id=int(env('OWNER_ID'))
        ),
        db=Database(
            db_name=env('DB_NAME'),
            db_host=env('DB_HOST'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD')
        )
    )
