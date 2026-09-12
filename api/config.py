from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Onion Byte"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "onion_byte"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    
    REDIS_URL: str = "redis://localhost:6379"
    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    @property
    def DATABASE_URL(self) -> str:
        import os
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            if env_url.startswith("postgres://"):
                env_url = env_url.replace("postgres://", "postgresql+asyncpg://", 1)
            elif env_url.startswith("postgresql://"):
                env_url = env_url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return env_url
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
