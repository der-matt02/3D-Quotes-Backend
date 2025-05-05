from pydantic import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    mongo_db: str
    jwt_secret: str
    jwt_algorithm: str

    class Config:
        env_file = ".env"

settings = Settings()
