from enum import Enum
from typing import Optional

from pydantic import BaseSettings, SecretStr


class Env(Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class EODCSettings(BaseSettings):
    ENVIRONMENT: Env = Env.DEVELOPMENT
    BASE_URL: Optional[str] = None
    FAAS_URL: Optional[str] = None
    DASK_URL: Optional[str] = None
    API_KEY: Optional[SecretStr] = None

    @property
    def NAMESPACE(self):
        return "development" if self.ENVIRONMENT == Env.DEVELOPMENT else "production"


settings = EODCSettings()
