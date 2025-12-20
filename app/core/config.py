from  pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = True
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 2880
    
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    class Config:
        env_file = ".env"
        # Forcer Pydantic à convertir automatiquement certaines valeurs
        @classmethod
        def parse_env_var(cls, name, value):
            if name in {"MAIL_STARTTLS", "MAIL_SSL_TLS"}:
                return value.lower() in {"1", "true", "yes"}
            return value

settings = Settings()
