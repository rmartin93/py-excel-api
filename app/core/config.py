"""
Configuration management for the Excel API application.
Uses Pydantic BaseSettings for type-safe environment variable handling.

This is similar to environment configuration in Node.js, but with automatic
type validation and environment variable loading.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file.

    Similar to how you might use dotenv in Node.js, but with automatic
    type conversion and validation.
    """

    # Application settings
    app_name: str = "Python Excel API"
    app_version: str = "1.0.0"
    debug: bool = True

    # API settings
    api_prefix: str = "/api"
    host: str = "127.0.0.1"
    port: int = 8000

    # Directory paths
    templates_dir: str = "./templates"
    logs_dir: str = "./logs"

    # Logging configuration
    log_level: str = "DEBUG"
    log_file_rotation: bool = True
    log_max_bytes: int = 10_000_000  # 10MB
    log_backup_count: int = 5

    # CORS settings (for future use)
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8080"]
    cors_allow_credentials: bool = True

    model_config = SettingsConfigDict(
        # This tells Pydantic to load from .env file
        env_file=".env",
        env_file_encoding="utf-8",
        # Case insensitive environment variables
        case_sensitive=False
    )


# Create a global instance (similar to exporting config object in Node.js)
settings = Settings()


def get_settings() -> Settings:
    """Dependency function for FastAPI to inject settings.

    This pattern allows for easy testing and dependency injection,
    similar to how you might inject config in Express middleware.
    """
    return settings
