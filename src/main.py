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
from src import states
from src.services.logging_config import get_logger
from src.handlers.start import (
    start_command,
    language_callback,
)
from src.handlers.diagnosis import (
    start_diagnosis_callback,
    pain_q1_callback,
    pain_q2_callback,
    pain_q3_callback,
    readiness_callback,
    proceed_to_recommendation_callback,
    review_edit_q1_callback,
    review_edit_q2_callback,
    review_edit_q3_callback,
    review_edit_readiness_callback,
    diag_back_q1_callback,
    diag_back_q2_callback,
    diag_back_q3_callback,
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
    edit_form_menu_callback,
    edit_field_name_callback,
    edit_field_phone_callback,
    edit_field_email_callback,
    edit_field_business_callback,
    back_to_summary_callback,
    handle_edit_name,
    handle_edit_phone,
    handle_edit_email,
    handle_edit_business,
)
from src.handlers.commands import (
    restart_command,
    language_command,
    setup_bot_commands,
)

logger = get_logger(__name__)


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
            states.LANGUAGE_SELECT: [
                CallbackQueryHandler(language_callback, pattern=r"^lang_(zh|en)$"),
            ],
            states.POSITIONING: [
                CallbackQueryHandler(
                    start_diagnosis_callback, pattern=r"^start_diagnosis$"
                ),
            ],
            states.Q1: [
                CallbackQueryHandler(pain_q1_callback, pattern=r"^pain_q1_[abcd]$"),
            ],
            states.Q2: [
                CallbackQueryHandler(pain_q2_callback, pattern=r"^pain_q2_[abcd]$"),
                CallbackQueryHandler(diag_back_q1_callback, pattern=r"^diag_back_q1$"),
            ],
            states.Q3: [
                CallbackQueryHandler(pain_q3_callback, pattern=r"^pain_q3_[abcd]$"),
                CallbackQueryHandler(diag_back_q2_callback, pattern=r"^diag_back_q2$"),
            ],
            states.READINESS: [
                CallbackQueryHandler(readiness_callback, pattern=r"^readiness_[abcd]$"),
                CallbackQueryHandler(diag_back_q3_callback, pattern=r"^diag_back_q3$"),
            ],
            states.REVIEW_ANSWERS: [
                CallbackQueryHandler(
                    proceed_to_recommendation_callback,
                    pattern=r"^proceed_to_recommendation$",
                ),
                CallbackQueryHandler(
                    review_edit_q1_callback, pattern=r"^review_edit_q1$"
                ),
                CallbackQueryHandler(
                    review_edit_q2_callback, pattern=r"^review_edit_q2$"
                ),
                CallbackQueryHandler(
                    review_edit_q3_callback, pattern=r"^review_edit_q3$"
                ),
                CallbackQueryHandler(
                    review_edit_readiness_callback, pattern=r"^review_edit_readiness$"
                ),
            ],
            states.RECOMMENDATION: [
                CallbackQueryHandler(
                    select_starter_callback, pattern=r"^select_starter$"
                ),
                CallbackQueryHandler(select_core_callback, pattern=r"^select_core$"),
                CallbackQueryHandler(
                    apply_core_review_callback, pattern=r"^apply_core_review$"
                ),
            ],
            states.UPSELL_TEAM: [
                CallbackQueryHandler(
                    upsell_team_yes_callback, pattern=r"^upsell_team_yes$"
                ),
                CallbackQueryHandler(
                    upsell_team_no_callback, pattern=r"^upsell_team_no$"
                ),
            ],
            states.UPSELL_INTENT: [
                CallbackQueryHandler(
                    upsell_intent_scale_callback, pattern=r"^upsell_intent_scale$"
                ),
                CallbackQueryHandler(
                    upsell_intent_foundation_callback,
                    pattern=r"^upsell_intent_foundation$",
                ),
            ],
            states.REG_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name),
            ],
            states.REG_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone),
            ],
            states.REG_EMAIL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email),
            ],
            states.REG_BUSINESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_business_type),
            ],
            states.CONFIRMATION: [
                CallbackQueryHandler(
                    confirm_submit_callback, pattern=r"^confirm_submit$"
                ),
                CallbackQueryHandler(
                    edit_form_menu_callback, pattern=r"^edit_form_menu$"
                ),
            ],
            states.EDIT_FORM_MENU: [
                CallbackQueryHandler(
                    edit_field_name_callback, pattern=r"^edit_field_name$"
                ),
                CallbackQueryHandler(
                    edit_field_phone_callback, pattern=r"^edit_field_phone$"
                ),
                CallbackQueryHandler(
                    edit_field_email_callback, pattern=r"^edit_field_email$"
                ),
                CallbackQueryHandler(
                    edit_field_business_callback, pattern=r"^edit_field_business$"
                ),
                CallbackQueryHandler(
                    back_to_summary_callback, pattern=r"^back_to_summary$"
                ),
            ],
            states.EDIT_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_name),
            ],
            states.EDIT_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_phone),
            ],
            states.EDIT_EMAIL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_email),
            ],
            states.EDIT_BUSINESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_business),
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
        logger.info(
            "Bot commands registered successfully", extra={"event": "bot_startup"}
        )

    application.post_init = post_init

    # Start the bot
    logger.info("Starting ACPF bot...", extra={"event": "bot_startup"})
    application.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
