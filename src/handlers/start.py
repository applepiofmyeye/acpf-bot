"""Start and language selection handlers for ACPF Bot."""

from telegram import Update
from telegram.ext import ContextTypes

from src.config import WELCOME_IMAGE_PATH
from src.i18n.messages import WELCOME_MESSAGE, get_text
from src.keyboards.buttons import language_keyboard, start_diagnosis_keyboard
from src import states
from src.models.user_data import UserData


def init_user_data(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Initialize user data for a new session."""
    user_data = UserData(context)
    user_data.reset()


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

    return states.LANGUAGE_SELECT


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle language selection callback."""
    query = update.callback_query
    await query.answer()

    # Extract language from callback data
    lang = "zh" if query.data == "lang_zh" else "en"
    user_data = UserData(context)
    user_data.lang = lang

    # Send language confirmation
    await query.message.reply_text(get_text("languageChanged", lang))

    # Show positioning message
    return await show_positioning(update, context)


async def show_positioning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show positioning message with Start Diagnosis button."""
    user_data = UserData(context)
    lang = user_data.lang or "en"

    await update.callback_query.message.reply_text(
        get_text("positioning", lang),
        reply_markup=start_diagnosis_keyboard(lang),
    )

    return states.POSITIONING
