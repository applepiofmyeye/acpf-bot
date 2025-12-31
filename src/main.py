"""Main entry point for ACPF Telegram Bot."""

import sys
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from src.config import BOT_TOKEN, validate_config
from src.handlers.start import (
    start_command,
    language_callback,
    LANGUAGE_SELECT,
    POSITIONING,
    Q1,
    Q2,
    Q3,
    READINESS,
    RECOMMENDATION,
    UPSELL_TEAM,
    UPSELL_INTENT,
    REG_NAME,
    REG_PHONE,
    REG_EMAIL,
    REG_BUSINESS,
    CONFIRMATION,
)
from src.handlers.diagnosis import (
    start_diagnosis_callback,
    pain_q1_callback,
    pain_q2_callback,
    pain_q3_callback,
    readiness_callback,
)
from src.handlers.recommendation import (
    select_starter_callback,
    select_core_callback,
    apply_core_review_callback,
    upsell_team_yes_callback,
    upsell_team_no_callback,
    upsell_intent_scale_callback,
    upsell_intent_foundation_callback,
)
from src.handlers.registration import (
    handle_name,
    handle_phone,
    handle_email,
    handle_business_type,
    confirm_submit_callback,
    edit_form_callback,
)
from src.handlers.commands import (
    restart_command,
    language_command,
    setup_bot_commands,
)


def main() -> None:
    """Start the bot."""
    # Validate configuration
    if not validate_config():
        sys.exit(1)
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Build conversation handler
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_command),
        ],
        states={
            LANGUAGE_SELECT: [
                CallbackQueryHandler(language_callback, pattern=r"^lang_(zh|en)$"),
            ],
            POSITIONING: [
                CallbackQueryHandler(start_diagnosis_callback, pattern=r"^start_diagnosis$"),
            ],
            Q1: [
                CallbackQueryHandler(pain_q1_callback, pattern=r"^pain_q1_[abcd]$"),
            ],
            Q2: [
                CallbackQueryHandler(pain_q2_callback, pattern=r"^pain_q2_[abcd]$"),
            ],
            Q3: [
                CallbackQueryHandler(pain_q3_callback, pattern=r"^pain_q3_[abcd]$"),
            ],
            READINESS: [
                CallbackQueryHandler(readiness_callback, pattern=r"^readiness_[abcd]$"),
            ],
            RECOMMENDATION: [
                CallbackQueryHandler(select_starter_callback, pattern=r"^select_starter$"),
                CallbackQueryHandler(select_core_callback, pattern=r"^select_core$"),
                CallbackQueryHandler(apply_core_review_callback, pattern=r"^apply_core_review$"),
            ],
            UPSELL_TEAM: [
                CallbackQueryHandler(upsell_team_yes_callback, pattern=r"^upsell_team_yes$"),
                CallbackQueryHandler(upsell_team_no_callback, pattern=r"^upsell_team_no$"),
            ],
            UPSELL_INTENT: [
                CallbackQueryHandler(upsell_intent_scale_callback, pattern=r"^upsell_intent_scale$"),
                CallbackQueryHandler(upsell_intent_foundation_callback, pattern=r"^upsell_intent_foundation$"),
            ],
            REG_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name),
            ],
            REG_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone),
            ],
            REG_EMAIL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email),
            ],
            REG_BUSINESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_business_type),
            ],
            CONFIRMATION: [
                CallbackQueryHandler(confirm_submit_callback, pattern=r"^confirm_submit$"),
                CallbackQueryHandler(edit_form_callback, pattern=r"^edit_form$"),
            ],
        },
        fallbacks=[
            CommandHandler("start", start_command),
            CommandHandler("restart", restart_command),
            CommandHandler("language", language_command),
        ],
        per_user=True,
        per_chat=True,
    )
    
    # Add handlers
    application.add_handler(conv_handler)
    
    # Add standalone command handlers (for when not in conversation)
    application.add_handler(CommandHandler("restart", restart_command))
    application.add_handler(CommandHandler("language", language_command))
    
    # Set up bot commands on startup
    async def post_init(app: Application) -> None:
        await setup_bot_commands(app)
        print("Bot commands registered successfully")
    
    application.post_init = post_init
    
    # Start the bot
    print("Starting ACPF bot...")
    application.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()


