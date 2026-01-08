"""Configuration module for ACPF Bot."""

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Bot configuration
    bot_token: str = Field(..., description="Telegram Bot API token")
    admin_chat_id: str | None = Field(
        default=None, description="Telegram chat ID for admin notifications"
    )

    # Google Sheets configuration
    google_service_account_json: str | None = Field(
        default=None,
        description="Google Sheets service account credentials JSON (base64 or plain)",
    )
    spreadsheet_id: str | None = Field(
        default=None, description="Google Sheets spreadsheet ID"
    )
    sheet_name: str = Field(default="Sheet1", description="Google Sheets sheet name")

    # Logging configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    # Paths (computed properties)
    @property
    def base_dir(self) -> Path:
        """Get base directory."""
        return Path(__file__).parent.parent

    @property
    def assets_dir(self) -> Path:
        """Get assets directory."""
        return self.base_dir / "assets"

    @property
    def welcome_image_path(self) -> Path:
        """Get welcome image path."""
        return self.assets_dir / "welcome.jpg"


# Create global settings instance
settings = Settings()

# Export for backward compatibility
BOT_TOKEN = settings.bot_token
ADMIN_CHAT_ID = settings.admin_chat_id
GOOGLE_SERVICE_ACCOUNT_JSON = settings.google_service_account_json
SPREADSHEET_ID = settings.spreadsheet_id
SHEET_NAME = settings.sheet_name
LOG_LEVEL = settings.log_level
BASE_DIR = settings.base_dir
ASSETS_DIR = settings.assets_dir
WELCOME_IMAGE_PATH = settings.welcome_image_path


def validate_config() -> bool:
    """Validate that all required environment variables are set.

    Returns:
        True if configuration is valid, False otherwise
    """
    # Lazy import to avoid circular dependency
    from src.services.logging_config import get_logger

    logger = get_logger(__name__)

    # Pydantic Settings already validates required fields on instantiation
    # This function is kept for backward compatibility
    if not settings.bot_token:
        logger.error(
            "BOT_TOKEN environment variable is not set",
            extra={"event": "config_validation_failed"},
        )
        return False

    return True
