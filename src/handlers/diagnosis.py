"""Diagnosis question handlers for ACPF Bot."""

from telegram import Update
from telegram.ext import ContextTypes

from src.config import SCORING_RULES
from src.i18n.messages import get_nested_text
from src.keyboards.buttons import pain_question_keyboard, readiness_keyboard
from src.handlers.start import Q1, Q2, Q3, READINESS, RECOMMENDATION


async def start_diagnosis_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Start Diagnosis button - begin Q1."""
    query = update.callback_query
    await query.answer()
    
    return await ask_pain_q1(update, context)


async def ask_pain_q1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask pain point question 1."""
    lang = context.user_data.get("lang", "en")
    question = get_nested_text(lang, "painQuestions", "q1", "question")
    
    await update.callback_query.message.reply_text(
        question,
        reply_markup=pain_question_keyboard("q1", lang),
    )
    
    return Q1


async def pain_q1_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Q1 answer."""
    query = update.callback_query
    await query.answer()
    
    # Extract answer (a, b, c, or d)
    answer = query.data.split("_")[-1]
    context.user_data["pain_answers"]["q1"] = answer
    
    # Update score
    score_type = SCORING_RULES["q1"].get(answer, "starter")
    if score_type == "starter":
        context.user_data["starter_score"] += 1
    else:
        context.user_data["core_score"] += 1
    
    return await ask_pain_q2(update, context)


async def ask_pain_q2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask pain point question 2."""
    lang = context.user_data.get("lang", "en")
    question = get_nested_text(lang, "painQuestions", "q2", "question")
    
    await update.callback_query.message.reply_text(
        question,
        reply_markup=pain_question_keyboard("q2", lang),
    )
    
    return Q2


async def pain_q2_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Q2 answer."""
    query = update.callback_query
    await query.answer()
    
    # Extract answer
    answer = query.data.split("_")[-1]
    context.user_data["pain_answers"]["q2"] = answer
    
    # Update score
    score_type = SCORING_RULES["q2"].get(answer, "starter")
    if score_type == "starter":
        context.user_data["starter_score"] += 1
    else:
        context.user_data["core_score"] += 1
    
    return await ask_pain_q3(update, context)


async def ask_pain_q3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask pain point question 3."""
    lang = context.user_data.get("lang", "en")
    question = get_nested_text(lang, "painQuestions", "q3", "question")
    
    await update.callback_query.message.reply_text(
        question,
        reply_markup=pain_question_keyboard("q3", lang),
    )
    
    return Q3


async def pain_q3_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Q3 answer."""
    query = update.callback_query
    await query.answer()
    
    # Extract answer
    answer = query.data.split("_")[-1]
    context.user_data["pain_answers"]["q3"] = answer
    
    # Update score
    score_type = SCORING_RULES["q3"].get(answer, "starter")
    if score_type == "starter":
        context.user_data["starter_score"] += 1
    else:
        context.user_data["core_score"] += 1
    
    return await ask_readiness(update, context)


async def ask_readiness(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask readiness question."""
    lang = context.user_data.get("lang", "en")
    question = get_nested_text(lang, "readinessQuestion", "question")
    
    await update.callback_query.message.reply_text(
        question,
        reply_markup=readiness_keyboard(lang),
    )
    
    return READINESS


async def readiness_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle readiness answer and calculate recommendation."""
    query = update.callback_query
    await query.answer()
    
    # Extract answer
    answer = query.data.split("_")[-1]
    context.user_data["readiness"] = answer
    
    # Update score
    score_type = SCORING_RULES["readiness"].get(answer, "starter")
    if score_type == "starter":
        context.user_data["starter_score"] += 1
    else:
        context.user_data["core_score"] += 1
    
    # Calculate recommendation
    # Core wins only if core_score > starter_score (tie favors Starter)
    if context.user_data["core_score"] > context.user_data["starter_score"]:
        context.user_data["recommendation"] = "core"
    else:
        context.user_data["recommendation"] = "starter"
    
    # Import here to avoid circular import
    from src.handlers.recommendation import show_recommendation
    return await show_recommendation(update, context)

