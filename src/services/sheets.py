"""Google Sheets integration for ACPF Bot."""

import json
from typing import List

import gspread
from google.oauth2.service_account import Credentials

from src.config import GOOGLE_SERVICE_ACCOUNT_JSON, SPREADSHEET_ID, SHEET_NAME

# Cache the client
_sheets_client = None


def get_google_sheets_client() -> gspread.Client:
    """Get or create Google Sheets client."""
    global _sheets_client
    
    if _sheets_client is not None:
        return _sheets_client
    
    if not GOOGLE_SERVICE_ACCOUNT_JSON:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON environment variable is not set")
    
    # Parse the JSON credentials
    credentials_dict = json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
    
    # Create credentials with required scopes
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    
    credentials = Credentials.from_service_account_info(
        credentials_dict,
        scopes=scopes,
    )
    
    # Create and cache the client
    _sheets_client = gspread.authorize(credentials)
    
    return _sheets_client


async def append_lead_row(row_data: List[str]) -> None:
    """Append a lead row to the Google Sheet.
    
    Args:
        row_data: List of values for columns A-L:
            [Timestamp, Language, TG User ID, TG Username, Full Name,
             Phone, Email, Business Type, Track, Program, Pain Point, Source]
    """
    if not SPREADSHEET_ID:
        raise ValueError("SPREADSHEET_ID environment variable is not set")
    
    try:
        client = get_google_sheets_client()
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        
        # Append the row
        worksheet.append_row(
            row_data,
            value_input_option="USER_ENTERED",
            insert_data_option="INSERT_ROWS",
        )
    except gspread.exceptions.SpreadsheetNotFound:
        raise ValueError(f"Spreadsheet with ID '{SPREADSHEET_ID}' not found. Make sure it's shared with the service account.")
    except gspread.exceptions.WorksheetNotFound:
        raise ValueError(f"Worksheet '{SHEET_NAME}' not found in the spreadsheet.")
    except Exception as e:
        raise RuntimeError(f"Failed to append row to Google Sheets: {e}")


