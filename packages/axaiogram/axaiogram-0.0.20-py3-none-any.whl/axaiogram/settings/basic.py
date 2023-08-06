from pydantic import BaseSettings


class BasicSettings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_ID: str
