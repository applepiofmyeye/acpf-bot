"""Start and language selection handlers for ACPF Bot."""

from telegram import Update
from telegram.ext import ContextTypes

from src.config import WELCOME_IMAGE_PATH
from src.i18n.messages import WELCOME_MESSAGE, get_text
from src.keyboards.buttons import language_keyboard, start_diagnosis_keyboard

# Conversation states
LANGUAGE_SELECT = 0
POSITIONING = 1
Q1 = 2
Q2 = 3
Q3 = 4
READINESS = 5
RECOMMENDATION = 6
GATE_QUESTION = 7
UPSELL_TEAM = 8
UPSELL_INTENT = 9
REG_NAME = 10
REG_PHONE = 11
REG_EMAIL = 12
REG_BUSINESS = 13
CONFIRMATION = 14


def init_user_data(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Initialize user data for a new session."""
    context.user_data["lang"] = None
    context.user_data["track"] = None
    context.user_data["program"] = None
    context.user_data["recommendation"] = None
    context.user_data["pain_answers"] = {"q1": None, "q2": None, "q3": None}
    context.user_data["readiness"] = None
    context.user_data["upsell_answers"] = {"has_team": None, "intent": None}
    context.user_data["form_data"] = {
        "full_name": None,
        "phone": None,
        "email": None,
        "business_type": None,
    }
    context.user_data["starter_score"] = 0
    context.user_data["core_score"] = 0


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /start command - show welcome image and language selection."""
    # Initialize user data
    init_user_data(context)
    
    # Build welcome message (bilingual)
    welcome_text = f"{WELCOME_MESSAGE['en']}\n\n{WELCOME_MESSAGE['zh']}"
    
    # Try to send welcome image, fallback to text only
    try:
        if WELCOME_IMAGE_PATH.exists():
            await update.message.reply_photo(
                photo=open(WELCOME_IMAGE_PATH, "rb"),
                caption=welcome_text,
                reply_markup=language_keyboard(),
            )
        else:
            # No image available, send text with language selection
            await update.message.reply_text(
                welcome_text,
                reply_markup=language_keyboard(),
            )
    except Exception:
        # Fallback to text only
        await update.message.reply_text(
            welcome_text,
            reply_markup=language_keyboard(),
        )
    
    return LANGUAGE_SELECT


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle language selection callback."""
    query = update.callback_query
    await query.answer()
    
    # Extract language from callback data
    lang = "zh" if query.data == "lang_zh" else "en"
    context.user_data["lang"] = lang
    
    # Send language confirmation
    await query.message.reply_text(get_text("languageChanged", lang))
    
    # Show positioning message
    return await show_positioning(update, context)


async def show_positioning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show positioning message with Start Diagnosis button."""
    lang = context.user_data.get("lang", "en")
    
    await update.callback_query.message.reply_text(
        get_text("positioning", lang),
        reply_markup=start_diagnosis_keyboard(lang),
    )
    
    return POSITIONING

