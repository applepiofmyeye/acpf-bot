# ACPF Telegram Bot

A dual-language (Chinese/English) Telegram bot for converting high-level beauty industry business owners into paid programs.

## Programs

- **Starter**: RM588 (runs every 2 months)
- **Core**: RM5,997 (runs twice a year: July and December)

## Features

- Bilingual support (Chinese/English)
- Welcome image with custom message
- Diagnostic questionnaire with scoring logic
- Program recommendation based on user responses
- Registration form with validation
- Google Sheets integration for lead tracking
- Admin notifications for new leads and errors
- Persistent menu button with commands

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Telegram Bot Token (from @BotFather)
BOT_TOKEN=your_telegram_bot_token

# Google Sheets Configuration
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"..."}
SPREADSHEET_ID=your_google_sheet_id
SHEET_NAME=Sheet1

# Admin Telegram User ID (for notifications)
ADMIN_CHAT_ID=your_telegram_user_id
```

### 3. Welcome Image

Place your welcome image at `assets/welcome.jpg`. The bot will display this image when users start the conversation.

### 4. Google Sheets Setup

1. Create a new Google Sheet
2. Share it with the service account email (found in JSON under `client_email`)
3. The sheet will receive rows with these columns:

| Column | Field |
|--------|-------|
| A | Timestamp |
| B | Language |
| C | Telegram User ID |
| D | Telegram Username |
| E | Full Name |
| F | Phone (WhatsApp) |
| G | Email |
| H | Beauty Business Type |
| I | Track (Starter / Core / CoreReview) |
| J | Program Selected |
| K | Key Pain Point |
| L | Source |

## How to Get Required Values

### BOT_TOKEN
1. Open Telegram and search for @BotFather
2. Send `/newbot` and follow the prompts
3. Copy the token provided

### GOOGLE_SERVICE_ACCOUNT_JSON
1. Go to Google Cloud Console
2. Create or select a project
3. Enable the Google Sheets API
4. Go to Credentials > Create Credentials > Service Account
5. Create the service account
6. Click on the service account > Keys > Add Key > Create new key > JSON
7. Copy the entire contents of the JSON file

### SPREADSHEET_ID
The SPREADSHEET_ID is in the URL: `docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`

### ADMIN_CHAT_ID
1. Search for @userinfobot on Telegram
2. Start a chat and send any message
3. It will reply with your user ID

## Running the Bot

```bash
python -m src.main
```

## Bot Commands

- `/start` - Start the bot and select language
- `/language` - Change language preference
- `/restart` - Clear session and start over

## Bot Flow

```
/start
  ↓
Welcome Image + Message
  ↓
Language Selection (中文 / English)
  ↓
Positioning Message
  ↓
Diagnostic Questions (Q1-Q4)
  ↓
Scoring & Recommendation
  ↓
├── Starter Path → Registration Form
└── Core Path → Gate Question → Registration Form
  ↓
Confirmation Summary
  ↓
Submit to Google Sheets
  ↓
Payment Instructions + Admin Notification
```

## Scoring Logic

| Question | Option A | Option B | Option C | Option D |
|----------|----------|----------|----------|----------|
| Q1 | Starter | Core | Core | Core |
| Q2 | Starter | Core | Core | Core |
| Q3 | Starter | Core | Core | Core |
| Readiness | Starter | Starter | Core | Core |

- If `core_score > starter_score` → Recommend Core
- If `starter_score >= core_score` → Recommend Starter (tie favors Starter)

## Project Structure

```
acpf-bot/
├── pyproject.toml          # Project config and dependencies
├── .env                    # Environment variables (create this)
├── README.md               # This file
├── assets/
│   └── welcome.jpg         # Welcome image (add this)
├── src/
│   ├── __init__.py
│   ├── main.py             # Entry point
│   ├── config.py           # Configuration
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py        # /start, language selection
│   │   ├── diagnosis.py    # Q1-Q4 questions
│   │   ├── recommendation.py # Recommendations, gate, upsell
│   │   ├── registration.py # Form collection
│   │   └── commands.py     # /restart, /language
│   ├── keyboards/
│   │   ├── __init__.py
│   │   └── buttons.py      # Inline keyboard builders
│   ├── services/
│   │   ├── __init__.py
│   │   ├── sheets.py       # Google Sheets integration
│   │   └── notifications.py # Admin notifications
│   └── i18n/
│       ├── __init__.py
│       └── messages.py     # Bilingual messages
└── questions.md            # Question flow reference
```

## License

MIT
