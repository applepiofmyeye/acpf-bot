"""Recommendation, gate question, and upsell handlers for ACPF Bot."""

from telegram import Update
from telegram.ext import ContextTypes

from src.i18n.messages import get_text, get_nested_text
from src.keyboards.buttons import (
    starter_recommendation_keyboard,
    core_recommendation_keyboard,
    upsell_team_keyboard,
    upsell_intent_keyboard,
    upsell_rejected_keyboard,
)
from src import states
from src.enums import ProgramType
from src.models.user_data import UserData
from src.services.upsell import UpsellQualifier
from src.services.logging_config import get_logger
from src.handlers.registration import start_form

logger = get_logger(__name__)


async def show_recommendation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Show program recommendation based on scoring."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    recommendation_str = (
        ProgramType.CORE.value
    )  # Push for Professional Certificate Beauty Management Strategy
    user = (
        update.callback_query.from_user
        if update.callback_query
        else update.effective_user
    )

    logger.info(
        "Recommendation shown",
        extra={
            "event": "recommendation_shown",
            "telegram_user_id": user.id if user else None,
            "state": "RECOMMENDATION",
            "recommendation": recommendation_str,
        },
    )

    if recommendation_str == ProgramType.CORE.value:
        rec = get_nested_text(lang, "recommendCore")
        await update.callback_query.message.reply_text(
            rec.get("message", ""),
            reply_markup=core_recommendation_keyboard(lang),
        )
    else:
        rec = get_nested_text(lang, "recommendStarter")
        await update.callback_query.message.reply_text(
            rec.get("message", ""),
            reply_markup=starter_recommendation_keyboard(lang),
        )

    return states.RECOMMENDATION


async def select_starter_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle Starter selection - proceed to registration."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    user_data.track = ProgramType.STARTER.value
    user_data.program = ProgramType.STARTER.value

    logger.info(
        "Starter program selected",
        extra={
            "event": "program_selected",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "RECOMMENDATION",
            "program": ProgramType.STARTER.value,
        },
    )

    return await start_form(update, context)


async def select_core_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle Professional Certificate Beauty Management Strategy selection - proceed to registration."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    user_data.track = ProgramType.CORE.value
    user_data.program = ProgramType.CORE.value

    logger.info(
        "Professional Certificate Beauty Management Strategy program selected",
        extra={
            "event": "program_selected",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "RECOMMENDATION",
            "program": ProgramType.CORE.value,
        },
    )

    return await start_form(update, context)


async def apply_core_review_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle Professional Certificate Beauty Management Strategy Review application - start upsell flow."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    lang = user_data.lang or "en"
    user = query.from_user

    logger.info(
        "Professional Certificate Beauty Management Strategy Review request started",
        extra={
            "event": "core_review_request",
            "telegram_user_id": user.id,
            "state": "RECOMMENDATION",
        },
    )

    # Ask upsell question 1
    q = get_nested_text(lang, "upsellQuestions", "q1")

    logger.info(
        "Upsell question Q1 asked",
        extra={
            "event": "upsell_question_asked",
            "telegram_user_id": user.id,
            "state": "UPSELL_TEAM",
            "question": "q1",
        },
    )

    await query.message.reply_text(
        q.get("question", ""),
        reply_markup=upsell_team_keyboard(lang),
    )

    return states.UPSELL_TEAM


async def upsell_team_yes_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle upsell Q1 - has team."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    user_data.set_upsell_answer("has_team", True)

    logger.info(
        "Upsell question Q1 answer received",
        extra={
            "event": "upsell_answer_received",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "UPSELL_TEAM",
            "question": "q1",
            "answer": "has_team=True",
        },
    )

    return await ask_upsell_intent(update, context)


async def upsell_team_no_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle upsell Q1 - no team."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    user_data.set_upsell_answer("has_team", False)

    logger.info(
        "Upsell question Q1 answer received",
        extra={
            "event": "upsell_answer_received",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "UPSELL_TEAM",
            "question": "q1",
            "answer": "has_team=False",
        },
    )

    return await ask_upsell_intent(update, context)


async def ask_upsell_intent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask upsell question 2 - scale or foundation?"""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    q = get_nested_text(lang, "upsellQuestions", "q2")
    user = (
        update.callback_query.from_user
        if update.callback_query
        else update.effective_user
    )

    logger.info(
        "Upsell question Q2 asked",
        extra={
            "event": "upsell_question_asked",
            "telegram_user_id": user.id if user else None,
            "state": "UPSELL_INTENT",
            "question": "q2",
        },
    )

    await update.callback_query.message.reply_text(
        q.get("question", ""),
        reply_markup=upsell_intent_keyboard(lang),
    )

    return states.UPSELL_INTENT


async def upsell_intent_scale_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle upsell Q2 - wants to scale."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    user_data.set_upsell_answer("intent", "scale")
    lang = user_data.lang or "en"

    logger.info(
        "Upsell question Q2 answer received",
        extra={
            "event": "upsell_answer_received",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "UPSELL_INTENT",
            "question": "q2",
            "answer": "intent=scale",
        },
    )

    # Check if qualifies for Professional Certificate Beauty Management Strategy Review using UpsellQualifier
    qualifier = UpsellQualifier()
    if qualifier.qualifies_for_core_review(user_data):
        user_data.track = ProgramType.CORE_REVIEW.value
        user_data.program = ProgramType.CORE.value

        user = query.from_user
        logger.info(
            "Professional Certificate Beauty Management Strategy Review qualified",
            extra={
                "event": "core_review_qualified",
                "telegram_user_id": user.id,
                "state": "UPSELL_INTENT",
            },
        )

        await query.message.reply_text(get_text("upsellApproved", lang))

        return await start_form(update, context)
    else:
        logger.info(
            "Upsell qualification check failed",
            extra={
                "event": "upsell_qualification_failed",
                "telegram_user_id": query.from_user.id if query.from_user else None,
                "state": "UPSELL_INTENT",
            },
        )
        return await show_upsell_rejected(update, context)


async def upsell_intent_foundation_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle upsell Q2 - wants foundation."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    user_data.set_upsell_answer("intent", "foundation")

    logger.info(
        "Upsell question Q2 answer received",
        extra={
            "event": "upsell_answer_received",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "UPSELL_INTENT",
            "question": "q2",
            "answer": "intent=foundation",
        },
    )

    logger.info(
        "Upsell qualification check failed",
        extra={
            "event": "upsell_qualification_failed",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "UPSELL_INTENT",
        },
    )

    return await show_upsell_rejected(update, context)


async def show_upsell_rejected(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Show upsell rejection - recommend Starter."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    user = (
        update.callback_query.from_user
        if update.callback_query
        else update.effective_user
    )

    logger.info(
        "Upsell rejection shown",
        extra={
            "event": "upsell_rejected_shown",
            "telegram_user_id": user.id if user else None,
            "state": "RECOMMENDATION",
        },
    )

    await update.callback_query.message.reply_text(
        get_text("upsellRejected", lang),
        reply_markup=upsell_rejected_keyboard(lang),
    )

    return states.RECOMMENDATION
