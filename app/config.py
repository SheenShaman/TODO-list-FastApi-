from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str | None = None
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        if self.DB_URL:
            return self.DB_URL

        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
