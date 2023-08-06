from os.path import dirname, abspath, join

from typing import List, Optional

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

from cryptography.hazmat.primitives import serialization

import aiohttp

from plugins import token


BASE_DIR = dirname(dirname(dirname(abspath(__file__))))


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "rename"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost"]
    DOCS_URL: str = '/docs'

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    PUBLIC_JWT_KEY: Optional[str] = None
    JWT_ALGORITHM: str = 'RS256'
    api_token: Optional[str] = None

    AIOHTTP_SESSION: Optional[aiohttp.ClientSession] = None

    @property
    def aiohttp_session(self):
        if not self.AIOHTTP_SESSION:
            self.AIOHTTP_SESSION = aiohttp.ClientSession()
        return self.AIOHTTP_SESSION

    # def load_api_key(self):
    #     if not self.API_JWT_KEY:
    #         with open(join(BASE_DIR, 'api_key.key'), 'rb') as key_file:
    #             api_key = key_file.read(),
    #             self.API_JWT_KEY = api_key
    #     return self.API_JWT_KEY

    def load_privat_key(self):
        if not self.PRIVATE_JWT_KEY:
            with open(join(BASE_DIR, 'private_key.pem'), 'rb') as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=bytes(self.PEM_PASS, 'utf-8'),
                )
            self.PRIVATE_JWT_KEY = private_key
        return self.PRIVATE_JWT_KEY

    def load_public_key(self):
        if not self.PUBLIC_JWT_KEY:
            with open(join(BASE_DIR, 'public_key.pem'), 'rb') as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(),
                )
            self.PUBLIC_JWT_KEY = public_key
        return self.PUBLIC_JWT_KEY

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls,
        v: str | List[str]
    ) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


tags_metadata = [
    {
        "name": "rename",
        "description": "description",
    },
]

settings = Settings()
settings.load_public_key()
settings.load_privat_key()
# settings.load_api_key()

token_manager = token.TokenManager(
    None,
    settings.PUBLIC_JWT_KEY,
    settings.JWT_ALGORITHM,
)
