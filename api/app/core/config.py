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

    app_name: str = "K2 Service API"
    app_description: str = "Модуль обліку замовлень для K2 ERP-системи"
    debug: bool = False

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()

    database_url: str


settings = Settings()
