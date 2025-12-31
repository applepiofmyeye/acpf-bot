"""Command handlers for ACPF Bot."""

from telegram import Update, BotCommand
from telegram.ext import ContextTypes, ConversationHandler

from src.i18n.messages import get_text
from src.keyboards.buttons import language_keyboard
from src.handlers.start import init_user_data, LANGUAGE_SELECT


async def restart_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /restart command - clear session and start over."""
    lang = context.user_data.get("lang", "en")
    
    # Keep language preference but reset everything else
    init_user_data(context)
    context.user_data["lang"] = lang
    
    await update.message.reply_text(get_text("sessionCleared", lang))
    
    return ConversationHandler.END


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /language command - change language preference."""
    lang = context.user_data.get("lang", "en")
    
    await update.message.reply_text(
        get_text("languagePrompt", lang),
        reply_markup=language_keyboard(),
    )
    
    return LANGUAGE_SELECT


async def setup_bot_commands(application) -> None:
    """Set up persistent menu commands with BotFather."""
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("language", "Change language / 更改语言"),
        BotCommand("restart", "Start over / 重新开始"),
    ]
    
    await application.bot.set_my_commands(commands)


