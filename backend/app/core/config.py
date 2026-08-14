from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "OpenTrade"
    app_env: str = "development"
    debug: bool = False

    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    initial_virtual_balance: float = 100000.00

    @property
    def database_url(self) -> str:
        return(
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"


settings = Settings()