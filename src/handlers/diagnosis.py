"""Diagnosis question handlers for ACPF Bot."""

import re
from telegram import Update
from telegram.ext import ContextTypes

from src.i18n.messages import get_nested_text
from src.keyboards.buttons import pain_question_keyboard, readiness_keyboard
from src import states
from src.enums import ReadinessAnswer
from src.models.user_data import UserData
from src.services.scoring import ScoreCalculator
from src.handlers.recommendation import show_recommendation


def parse_pain_answer(callback_data: str) -> tuple[str, str]:
    """Parse pain question callback data.

    Args:
        callback_data: Callback data string (e.g., "pain_q1_a", "pain_q2_b")

    Returns:
        Tuple of (question_num, answer) e.g., ("q1", "a")

    Raises:
        ValueError: If callback_data format is invalid
    """
    match = re.match(r"^pain_(q[123])_([abcd])$", callback_data)
    if not match:
        raise ValueError(f"Invalid pain answer callback_data: {callback_data}")
    return match.group(1), match.group(2)


def parse_readiness_answer(callback_data: str) -> ReadinessAnswer:
    """Parse readiness question callback data.

    Args:
        callback_data: Callback data string (e.g., "readiness_a", "readiness_b")

    Returns:
        ReadinessAnswer enum

    Raises:
        ValueError: If callback_data format is invalid
    """
    match = re.match(r"^readiness_([abcd])$", callback_data)
    if not match:
        raise ValueError(f"Invalid readiness answer callback_data: {callback_data}")
    answer_str = match.group(1)
    return ReadinessAnswer(answer_str)


async def start_diagnosis_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle Start Diagnosis button - begin Q1."""
    query = update.callback_query
    await query.answer()

    return await ask_pain_question(update, context, "q1", states.Q1)


async def ask_pain_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    question_num: str,
    next_state: int,
) -> int:
    """Ask a pain point question (generic function for DRY)."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    question = get_nested_text(lang, "painQuestions", question_num, "question")

    await update.callback_query.message.reply_text(
        question,
        reply_markup=pain_question_keyboard(question_num, lang),
    )

    return next_state


async def handle_pain_answer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    question_num: str,
    next_question: str,
    next_state: int,
) -> int:
    """Handle pain point answer (generic function for DRY)."""
    query = update.callback_query
    await query.answer()

    # Parse callback data using regex for robust extraction
    parsed_question, answer = parse_pain_answer(query.data)

    # Validate that parsed question matches expected question_num
    if parsed_question != question_num:
        raise ValueError(
            f"Question mismatch: expected {question_num}, got {parsed_question} "
            f"from callback_data: {query.data}"
        )

    user_data = UserData(context)
    user_data.set_pain_answer(question_num, answer)

    # Update score using ScoreCalculator
    score_calculator = ScoreCalculator(user_data)
    score_calculator.update_score(question_num, answer)

    # Ask next question - readiness is handled differently
    if next_question == "readiness":
        return await ask_readiness(update, context)
    else:
        return await ask_pain_question(update, context, next_question, next_state)


async def ask_pain_q1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask pain point question 1."""
    return await ask_pain_question(update, context, "q1", states.Q1)


async def pain_q1_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Q1 answer."""
    return await handle_pain_answer(update, context, "q1", "q2", states.Q2)


async def ask_pain_q2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask pain point question 2."""
    return await ask_pain_question(update, context, "q2", states.Q2)


async def pain_q2_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Q2 answer."""
    return await handle_pain_answer(update, context, "q2", "q3", states.Q3)


async def ask_pain_q3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask pain point question 3."""
    return await ask_pain_question(update, context, "q3", states.Q3)


async def pain_q3_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Q3 answer."""
    return await handle_pain_answer(
        update, context, "q3", "readiness", states.READINESS
    )


async def ask_readiness(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask readiness question."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    question = get_nested_text(lang, "readinessQuestion", "question")

    await update.callback_query.message.reply_text(
        question,
        reply_markup=readiness_keyboard(lang),
    )

    return states.READINESS


async def readiness_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle readiness answer and calculate recommendation."""
    query = update.callback_query
    await query.answer()

    # Parse callback data using regex for robust extraction
    answer = parse_readiness_answer(query.data)

    user_data = UserData(context)
    user_data.readiness = answer

    # Update score using ScoreCalculator (needs string value for scoring rules)
    score_calculator = ScoreCalculator(user_data)
    score_calculator.update_score("readiness", answer.value)

    # Calculate recommendation
    recommendation = score_calculator.calculate_recommendation()
    user_data.recommendation = recommendation.value  # Store as string for compatibility

    # Show recommendation
    return await show_recommendation(update, context)
