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
from src.handlers.registration import start_form


async def show_recommendation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Show program recommendation based on scoring."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    recommendation_str = user_data.recommendation or ProgramType.STARTER.value

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

    return await start_form(update, context)


async def select_core_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle Core selection - proceed to registration."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    user_data.track = ProgramType.CORE.value
    user_data.program = ProgramType.CORE.value

    return await start_form(update, context)


async def apply_core_review_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle Core Review application - start upsell flow."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    lang = user_data.lang or "en"

    # Ask upsell question 1
    q = get_nested_text(lang, "upsellQuestions", "q1")
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

    return await ask_upsell_intent(update, context)


async def upsell_team_no_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle upsell Q1 - no team."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    user_data.set_upsell_answer("has_team", False)

    return await ask_upsell_intent(update, context)


async def ask_upsell_intent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask upsell question 2 - scale or foundation?"""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    q = get_nested_text(lang, "upsellQuestions", "q2")

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

    # Check if qualifies for Core Review using UpsellQualifier
    qualifier = UpsellQualifier()
    if qualifier.qualifies_for_core_review(user_data):
        user_data.track = ProgramType.CORE_REVIEW.value
        user_data.program = ProgramType.CORE.value

        await query.message.reply_text(get_text("upsellApproved", lang))

        return await start_form(update, context)
    else:
        return await show_upsell_rejected(update, context)


async def upsell_intent_foundation_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle upsell Q2 - wants foundation."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    user_data.set_upsell_answer("intent", "foundation")

    return await show_upsell_rejected(update, context)


async def show_upsell_rejected(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Show upsell rejection - recommend Starter."""
    user_data = UserData(context)
    lang = user_data.lang or "en"

    await update.callback_query.message.reply_text(
        get_text("upsellRejected", lang),
        reply_markup=upsell_rejected_keyboard(lang),
    )

    return states.RECOMMENDATION
