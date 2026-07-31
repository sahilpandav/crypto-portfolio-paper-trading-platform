from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "OpenTrade"
    app_env: str = "development"
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()