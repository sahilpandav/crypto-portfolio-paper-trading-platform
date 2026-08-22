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
    test_db_name: str = "opentrade_test_db"


    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    initial_virtual_balance: float = 100000.00

    binance_api_base_url: str = "https://api.binance.com"

    @property
    def database_url(self) -> str:
        return(
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def test_database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.test_db_name}"
        )

    class Config:
        env_file = ".env"


settings = Settings()