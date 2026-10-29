from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "dev"
    namespace: str = "idp-dev"
    kubeconfig: str | None = None

    class Config:
        env_prefix = "IDP_"


settings = Settings()
