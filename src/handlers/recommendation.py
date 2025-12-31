"""Recommendation, gate question, and upsell handlers for ACPF Bot."""

from telegram import Update
from telegram.ext import ContextTypes

from src.config import ADMIN_CHAT_ID
from src.i18n.messages import get_text, get_nested_text
from src.keyboards.buttons import (
    starter_recommendation_keyboard,
    core_recommendation_keyboard,
    gate_question_keyboard,
    gate_rejection_keyboard,
    upsell_team_keyboard,
    upsell_intent_keyboard,
    upsell_rejected_keyboard,
)
from src.handlers.start import (
    RECOMMENDATION,
    GATE_QUESTION,
    UPSELL_TEAM,
    UPSELL_INTENT,
    REG_NAME,
)


async def show_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show program recommendation based on scoring."""
    lang = context.user_data.get("lang", "en")
    recommendation = context.user_data.get("recommendation", "starter")
    
    if recommendation == "core":
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
    
    return RECOMMENDATION


async def select_starter_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Starter selection - proceed to registration."""
    query = update.callback_query
    await query.answer()
    
    context.user_data["track"] = "starter"
    context.user_data["program"] = "starter"
    
    # Import here to avoid circular import
    from src.handlers.registration import start_form
    return await start_form(update, context)


async def select_core_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Core selection - show gate question."""
    query = update.callback_query
    await query.answer()
    
    context.user_data["track"] = "core"
    lang = context.user_data.get("lang", "en")
    
    await query.message.reply_text(
        get_text("gateQuestion", lang),
        reply_markup=gate_question_keyboard(lang),
    )
    
    return GATE_QUESTION


async def gate_yes_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle gate question 'Yes' - proceed to Core registration."""
    query = update.callback_query
    await query.answer()
    
    context.user_data["program"] = "core"
    
    from src.handlers.registration import start_form
    return await start_form(update, context)


async def gate_no_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle gate question 'No' - redirect to Starter."""
    query = update.callback_query
    await query.answer()
    
    lang = context.user_data.get("lang", "en")
    
    await query.message.reply_text(
        get_text("gateNoResponse", lang),
        reply_markup=gate_rejection_keyboard(lang),
    )
    
    return GATE_QUESTION


async def register_starter_fallback_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Starter registration after gate rejection."""
    query = update.callback_query
    await query.answer()
    
    context.user_data["track"] = "starter"
    context.user_data["program"] = "starter"
    
    from src.handlers.registration import start_form
    return await start_form(update, context)


async def apply_core_review_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Core Review application - start upsell flow."""
    query = update.callback_query
    await query.answer()
    
    lang = context.user_data.get("lang", "en")
    user = query.from_user
    
    # Notify admin about upsell request
    if ADMIN_CHAT_ID:
        try:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=(
                    f"🔔 Core Review Request\n\n"
                    f"User: @{user.username or 'N/A'} (ID: {user.id})\n"
                    f"Language: {'中文' if lang == 'zh' else 'English'}\n"
                    f"Status: Started upsell flow"
                ),
            )
        except Exception as e:
            print(f"Failed to notify admin about upsell: {e}")
    
    # Ask upsell question 1
    q = get_nested_text(lang, "upsellQuestions", "q1")
    await query.message.reply_text(
        q.get("question", ""),
        reply_markup=upsell_team_keyboard(lang),
    )
    
    return UPSELL_TEAM


async def upsell_team_yes_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle upsell Q1 - has team."""
    query = update.callback_query
    await query.answer()
    
    context.user_data["upsell_answers"]["has_team"] = True
    
    return await ask_upsell_intent(update, context)


async def upsell_team_no_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle upsell Q1 - no team."""
    query = update.callback_query
    await query.answer()
    
    context.user_data["upsell_answers"]["has_team"] = False
    
    return await ask_upsell_intent(update, context)


async def ask_upsell_intent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask upsell question 2 - scale or foundation?"""
    lang = context.user_data.get("lang", "en")
    q = get_nested_text(lang, "upsellQuestions", "q2")
    
    await update.callback_query.message.reply_text(
        q.get("question", ""),
        reply_markup=upsell_intent_keyboard(lang),
    )
    
    return UPSELL_INTENT


async def upsell_intent_scale_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle upsell Q2 - wants to scale."""
    query = update.callback_query
    await query.answer()
    
    context.user_data["upsell_answers"]["intent"] = "scale"
    lang = context.user_data.get("lang", "en")
    user = query.from_user
    
    # Check if qualifies for Core Review (has team + wants to scale)
    if context.user_data["upsell_answers"]["has_team"]:
        context.user_data["track"] = "coreReview"
        context.user_data["program"] = "core"
        
        # Notify admin about qualification
        if ADMIN_CHAT_ID:
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=(
                        f"✅ Core Review Qualified\n\n"
                        f"User: @{user.username or 'N/A'} (ID: {user.id})\n"
                        f"Has Team: Yes\n"
                        f"Intent: Scale\n"
                        f"Status: Approved for Core review"
                    ),
                )
            except Exception as e:
                print(f"Failed to notify admin: {e}")
        
        await query.message.reply_text(get_text("upsellApproved", lang))
        
        from src.handlers.registration import start_form
        return await start_form(update, context)
    else:
        return await show_upsell_rejected(update, context)


async def upsell_intent_foundation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle upsell Q2 - wants foundation."""
    query = update.callback_query
    await query.answer()
    
    context.user_data["upsell_answers"]["intent"] = "foundation"
    
    return await show_upsell_rejected(update, context)


async def show_upsell_rejected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show upsell rejection - recommend Starter."""
    lang = context.user_data.get("lang", "en")
    
    await update.callback_query.message.reply_text(
        get_text("upsellRejected", lang),
        reply_markup=upsell_rejected_keyboard(lang),
    )
    
    return RECOMMENDATION

