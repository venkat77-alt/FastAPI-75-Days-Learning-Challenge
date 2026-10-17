from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from pydantic import SecretStr
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str
    app_version: str
    port: int
    host: str
    app_debug: bool
    environment: str
    secret_key: SecretStr

settings = Settings()

print(settings.app_name)
print(settings.app_version)
print(settings.port)
print(settings.host)
print(settings.app_debug)
print(settings.environment)
print(settings.secret_key)
