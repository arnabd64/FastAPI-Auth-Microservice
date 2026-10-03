from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "sqlite:///app.db"
    DATABASE_CONSOLE_LOGS: bool = True

    # API Key settings
    KEY_PREFIX: str = "sk"
    KEY_LENGTH: int = 32

    # API router settings
    API_ROUTER_PREFIX: str = "/apikey"


settings = Settings()
