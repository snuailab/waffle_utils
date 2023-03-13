import json
import logging
import os
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "Waffle Store"

    VERSION: str = "0.1.0"
    # API_V1_STR: str = "/api/v1"

    HOST: str = None
    PORT: str = None

    LOG_CONF: str = os.path.abspath("./waffle_utils/log/.log_conf.json")

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# initialize logger
with open(settings.LOG_CONF) as json_file:
    conf = json.load(json_file)
    os.makedirs(os.path.split(conf["handlers"]["file"]["filename"])[0], exist_ok=True)
    logging.config.dictConfig(conf)

logger = logging.getLogger(__name__)
