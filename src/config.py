"""Configuration module for ACPF Bot."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# Google Sheets configuration
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME", "Sheet1")

# Paths
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
WELCOME_IMAGE_PATH = ASSETS_DIR / "welcome.jpg"

# Scoring rules for recommendation logic
SCORING_RULES = {
    "q1": {"a": "starter", "b": "core", "c": "core", "d": "core"},
    "q2": {"a": "starter", "b": "core", "c": "core", "d": "core"},
    "q3": {"a": "starter", "b": "core", "c": "core", "d": "core"},
    "readiness": {"a": "starter", "b": "starter", "c": "core", "d": "core"},
}

# Program labels
PROGRAM_LABELS = {
    "starter": "Starter",
    "core": "Core",
    "coreReview": "Core (Review)",
}

# Program prices (in RM)
PROGRAM_PRICES = {
    "starter": "588",
    "core": "5,997",
}


def validate_config() -> bool:
    """Validate that all required environment variables are set."""
    required = ["BOT_TOKEN"]
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        return False
    
    return True

