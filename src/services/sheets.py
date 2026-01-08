"""Google Sheets integration for ACPF Bot."""

import base64
import binascii
import json
from typing import List

import gspread
from google.oauth2.service_account import Credentials

from src.config import GOOGLE_SERVICE_ACCOUNT_JSON, SPREADSHEET_ID, SHEET_NAME
from src.services.logging_config import get_logger

logger = get_logger(__name__)

# Cache the client
_sheets_client = None


def _parse_credentials() -> dict:
    """Parse Google service account credentials from environment variable.

    Supports base64-encoded JSON (recommended) or plain JSON.

    Returns:
        Credentials dictionary for Google authentication

    Raises:
        ValueError: If credentials cannot be parsed
    """
    if not GOOGLE_SERVICE_ACCOUNT_JSON:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON environment variable is not set")

    value = GOOGLE_SERVICE_ACCOUNT_JSON.strip()

    if not value:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON is empty")

    # Try base64 decoding first (validate=False to be lenient with padding)
    try:
        decoded = base64.b64decode(value, validate=False)
        json_str = decoded.decode("utf-8")

        # Validate decoded string is not empty
        if not json_str.strip():
            raise ValueError("Base64 decoded to empty string")

        # Parse JSON
        return json.loads(json_str)

    except (binascii.Error, UnicodeDecodeError):
        # Not base64, try as plain JSON
        pass
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON after base64 decoding: {e}\n"
            f"Decoded value (first 200 chars): {json_str[:200] if 'json_str' in locals() else 'N/A'}"
        )

    # Try as plain JSON
    json_str = value

    # Remove quotes if wrapped
    if json_str.startswith('"') and json_str.endswith('"'):
        json_str = json_str[1:-1].replace('\\"', '"').replace("\\n", "\n")
    elif json_str.startswith("'") and json_str.endswith("'"):
        json_str = json_str[1:-1]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON format: {e}\n"
            f"Input (first 100 chars): {value[:100]}\n"
            f"Tip: Use base64 encoding: python encode_json.py your_credentials.json"
        )


def get_google_sheets_client() -> gspread.Client:
    """Get or create Google Sheets client.

    Returns:
        Authenticated gspread client

    Raises:
        ValueError: If credentials are invalid or missing
    """
    global _sheets_client

    if _sheets_client is not None:
        return _sheets_client

    # Parse credentials
    credentials_dict = _parse_credentials()

    # Create credentials object
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = Credentials.from_service_account_info(
        credentials_dict,
        scopes=scopes,
    )

    # Create and cache client
    _sheets_client = gspread.authorize(credentials)

    return _sheets_client


async def append_lead_row(row_data: List[str]) -> None:
    """Append a lead row to the Google Sheet.

    Column order:
        1. Timestamp (auto)
        2. Language (中文 / English)
        3. Telegram User ID
        4. Telegram Username
        5. Full Name
        6. Phone (WhatsApp)
        7. Email
        8. Beauty Business Type
        9. Current Stage (Exploring / Stuck / Scaling)
        10. Tier Interested (Entry / Core / Premium)
        11. Reason for Joining
        12. Source (Bot / Landing Page / Referral)

    Args:
        row_data: List of 12 string values matching the column order above

    Raises:
        ValueError: If SPREADSHEET_ID is not set or spreadsheet/worksheet not found
        RuntimeError: If row append fails
    """
    if not SPREADSHEET_ID:
        raise ValueError("SPREADSHEET_ID environment variable is not set")

    if len(row_data) != 12:
        raise ValueError(f"Expected 12 columns, got {len(row_data)}")

    try:
        client = get_google_sheets_client()
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)

        worksheet.append_row(
            row_data,
            value_input_option="USER_ENTERED",
            insert_data_option="INSERT_ROWS",
        )

        logger.info(
            "Lead row appended to Google Sheets",
            extra={
                "event": "sheet_append_success",
                "sheet_name": SHEET_NAME,
                "spreadsheet_id_suffix": SPREADSHEET_ID[-8:]
                if SPREADSHEET_ID
                else None,
            },
        )

    except gspread.exceptions.SpreadsheetNotFound as e:
        logger.error(
            "Spreadsheet not found",
            extra={
                "event": "sheet_error",
                "sheet_name": SHEET_NAME,
                "spreadsheet_id_suffix": SPREADSHEET_ID[-8:]
                if SPREADSHEET_ID
                else None,
            },
        )
        raise ValueError(
            f"Spreadsheet with ID '{SPREADSHEET_ID}' not found. "
            f"Make sure it's shared with the service account email."
        ) from e
    except gspread.exceptions.WorksheetNotFound as e:
        logger.error(
            "Worksheet not found",
            extra={
                "event": "sheet_error",
                "sheet_name": SHEET_NAME,
                "spreadsheet_id_suffix": SPREADSHEET_ID[-8:]
                if SPREADSHEET_ID
                else None,
            },
        )
        raise ValueError(
            f"Worksheet '{SHEET_NAME}' not found in the spreadsheet. "
            f"Available worksheets: {[ws.title for ws in spreadsheet.worksheets()]}"
        ) from e
    except Exception as e:
        logger.exception(
            "Failed to append row to Google Sheets",
            extra={
                "event": "sheet_error",
                "sheet_name": SHEET_NAME,
                "spreadsheet_id_suffix": SPREADSHEET_ID[-8:]
                if SPREADSHEET_ID
                else None,
            },
        )
        raise RuntimeError(f"Failed to append row to Google Sheets: {e}") from e
