from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv(".env", override=True)


class AppSettings(BaseSettings):
    IS_DEVELOPMENT: bool = True
    MONGODB_URI: str = Field(..., alias="mongo_uri") 
    TEXT_CHUNK_SIZE: int = 500
    TEXT_CHUNK_OVERLAP: int = 50
    
    BACKEND_CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["*"])
    
    UPSTASH_REDIS_REST_URL: str
    UPSTASH_REDIS_REST_TOKEN: str
    DEEPSEEK_API_KEY: str
    class Config:
        env_file = ".env"


settings = AppSettings()
