from enum import Enum

from pydantic import BaseSettings, SecretStr


class Env(Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class EODCSettings(BaseSettings):
    ENVIRONMENT: Env = Env.DEVELOPMENT
    BASE_URL: str = None
    FAAS_URL: str = None
    DASK_URL: str = None
    API_KEY: SecretStr = None

    @property
    def NAMESPACE(self):
        return "development" if self.ENVIRONMENT == Env.DEVELOPMENT else "production"


settings = EODCSettings()
