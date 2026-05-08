from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"

    clients: str = "/clients"
    products: str = "/products"
    orders: str = "/orders"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "FastAPI Blog"
    debug: bool = True

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()

    database_url: str
    frontend_url: str = "http://localhost:8000"

    media_dir: str = "media"

    max_upload_size_bytes: int = 5 * 1024 * 1024


settings = Settings()
