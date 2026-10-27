from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "IMHOTEP Bizarros Medical Secretary"
    secret_key: str = "change_me_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    database_url: str = "sqlite:///./imhotep.db"
    xerj_url: str = "http://localhost:9200"
    deep_human_families_site_url: str = (
        "https://make-deep-human-families-healthy.erichilarysmithsr.chatgpt.site"
    )
    openai_api_key: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
