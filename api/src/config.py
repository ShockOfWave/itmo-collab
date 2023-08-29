from pydantic import BaseSettings, AnyHttpUrl, Field, DirectoryPath


class Settings(BaseSettings):
    PROJECT_DIR_PATH: DirectoryPath = Field(env='PROJECT_DIR_PATH')

    S3_URL: AnyHttpUrl = Field('https://storage.yandexcloud.net', env='S3_URL')
    S3_BUCKET: str = Field('itmo-collab-petrol', env='S3_BUCKET')
    S3_ACCESS_KEY: str = Field(..., env='S3_ACCESS_KEY')
    S3_SECRET_KEY: str = Field(..., env='S3_SECRET_KEY')



settings = Settings()