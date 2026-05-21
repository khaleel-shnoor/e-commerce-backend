"""Application settings loaded from environment variables."""

from functools import lru_cache
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import Field, computed_field, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

from app.core.db_url import normalize_async_database_url

# Absolute path to backend/.env — works regardless of where the app is launched from.
_ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    """Central configuration for the SHNOOR API."""

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="SHNOOR API", alias="APP_NAME")
    app_env: Literal["development", "staging", "production"] = Field(
        default="development",
        alias="APP_ENV",
    )
    app_debug: bool = Field(default=False, alias="APP_DEBUG")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")  # noqa: S104
    app_port: int = Field(default=8000, alias="APP_PORT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    postgres_user: str = Field(default="postgres", alias="POSTGRES_USER")
    postgres_password: str = Field(default="postgres", alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(default="shnoor", alias="POSTGRES_DB")

    db_pool_size: int = Field(default=5, alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=10, alias="DB_MAX_OVERFLOW")

    secret_key: str = Field(default="change-me-in-production", alias="SECRET_KEY")
    jwt_secret_key: str | None = Field(default=None, alias="JWT_SECRET_KEY")
    jwt_refresh_secret_key: str | None = Field(default=None, alias="JWT_REFRESH_SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, alias="REFRESH_TOKEN_EXPIRE_DAYS")
    password_reset_expire_minutes: int = Field(default=60, alias="PASSWORD_RESET_EXPIRE_MINUTES")
    email_verification_expire_hours: int = Field(default=24, alias="EMAIL_VERIFICATION_EXPIRE_HOURS")

    @field_validator(
        "database_url",
        "jwt_secret_key",
        "jwt_refresh_secret_key",
        "google_client_id",
        "google_client_secret",
        mode="before",
    )
    @classmethod
    def empty_str_to_none(cls, value: str | None) -> str | None:
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        return value.strip() if isinstance(value, str) else value

    google_client_id: str | None = Field(default=None, alias="GOOGLE_CLIENT_ID")
    google_client_secret: str | None = Field(default=None, alias="GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = Field(
        default="http://localhost:8000/api/v1/auth/google/callback",
        alias="GOOGLE_REDIRECT_URI",
    )

    frontend_url: str = Field(default="http://localhost:5173", alias="FRONTEND_URL")

    smtp_enabled: bool = Field(default=False, alias="SMTP_ENABLED")
    smtp_host: str | None = Field(default=None, alias="SMTP_HOST")
    smtp_port: int = Field(default=587, alias="SMTP_PORT")
    smtp_secure: bool = Field(default=False, alias="SMTP_SECURE")
    smtp_user: str | None = Field(default=None, alias="SMTP_USER")
    smtp_password: str | None = Field(default=None, alias="SMTP_PASS")
    smtp_from: str | None = Field(default=None, alias="SMTP_FROM")

    cloudinary_cloud_name: str | None = Field(default=None, alias="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str | None = Field(default=None, alias="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str | None = Field(default=None, alias="CLOUDINARY_API_SECRET")
    cloudinary_folder: str = Field(default="shnoor", alias="CLOUDINARY_FOLDER")

    cors_origins: Annotated[
        list[str],
        NoDecode,
        Field(default_factory=lambda: ["http://localhost:5173"], alias="CORS_ORIGINS"),
    ]
    allowed_origins: Annotated[
        list[str] | None,
        NoDecode,
        Field(default=None, alias="ALLOWED_ORIGINS"),
    ]

    @staticmethod
    def _normalize_origin(origin: str) -> str:
        """Strip whitespace and trailing slash — browser Origin never includes a trailing slash."""
        return origin.strip().rstrip("/")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str] | None) -> list[str]:
        if value is None or value == "":
            return ["http://localhost:5173"]
        if isinstance(value, str):
            origins = value.split(",")
        else:
            origins = value
        return [cls._normalize_origin(o) for o in origins if o and o.strip()]

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: str | list[str] | None) -> list[str] | None:
        if value is None or value == "":
            return None
        if isinstance(value, str):
            origins = value.split(",")
        else:
            origins = value
        parsed = [cls._normalize_origin(o) for o in origins if o and o.strip()]
        return parsed or None

    @model_validator(mode="after")
    def merge_allowed_origins(self) -> "Settings":
        """ALLOWED_ORIGINS extends CORS_ORIGINS when set (Render-friendly alias)."""
        if self.allowed_origins:
            merged = list(dict.fromkeys([*self.cors_origins, *self.allowed_origins]))
            object.__setattr__(self, "cors_origins", merged)
        return self

    @computed_field  # type: ignore[prop-decorator]
    @property
    def effective_jwt_secret(self) -> str:
        """Access-token signing key (JWT_SECRET_KEY falls back to SECRET_KEY)."""
        return self.jwt_secret_key or self.secret_key

    @computed_field  # type: ignore[prop-decorator]
    @property
    def effective_jwt_refresh_secret(self) -> str:
        """Refresh-token signing key (falls back to JWT_SECRET_KEY then SECRET_KEY)."""
        return self.jwt_refresh_secret_key or self.jwt_secret_key or self.secret_key

    @computed_field  # type: ignore[prop-decorator]
    @property
    def async_database_url(self) -> str:
        """Resolved async PostgreSQL URL for SQLAlchemy + asyncpg."""
        url, _ = self._resolved_database()
        return url

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_connect_args(self) -> dict[str, Any]:
        """Extra connect_args for asyncpg (e.g. Neon SSL)."""
        _, connect_args = self._resolved_database()
        return connect_args

    def _resolved_database(self) -> tuple[str, dict[str, Any]]:
        if self.database_url:
            print("POSTGRES_USER =", self.postgres_user)
            return normalize_async_database_url(self.database_url)
        composed = (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
        return composed, {}

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def smtp_ready(self) -> bool:
        """True when SMTP is enabled and required credentials are present."""
        if not self.smtp_enabled:
            return False
        return bool(self.smtp_host and self.smtp_user and self.smtp_password and self.smtp_from)

    @property
    def cloudinary_ready(self) -> bool:
        return bool(
            self.cloudinary_cloud_name
            and self.cloudinary_api_key
            and self.cloudinary_api_secret
        )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
