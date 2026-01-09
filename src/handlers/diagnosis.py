"""Diagnosis question handlers for ACPF Bot."""

import re
from telegram import Update
from telegram.ext import ContextTypes

from src.i18n.messages import get_nested_text, get_text
from src.keyboards.buttons import (
    pain_question_keyboard,
    readiness_keyboard,
    review_answers_keyboard,
)
from src import states
from src.enums import ReadinessAnswer
from src.models.user_data import UserData
from src.services.scoring import ScoreCalculator
from src.services.logging_config import get_logger
from src.handlers.recommendation import show_recommendation

logger = get_logger(__name__)


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

    logger.info(
        "Diagnosis started",
        extra={
            "event": "diagnosis_started",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "POSITIONING",
        },
    )

    return await ask_pain_question(update, context, "q1", states.Q1)


async def ask_pain_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    question_num: str,
    next_state: int,
    show_back: bool = False,
) -> int:
    """Ask a pain point question (generic function for DRY).

    Args:
        update: Update object
        context: Context object
        question_num: Question number (q1, q2, q3)
        next_state: Next conversation state
        show_back: Whether to show back button (True for Q2, Q3)
    """
    user_data = UserData(context)
    lang = user_data.lang or "en"
    question = get_nested_text(lang, "painQuestions", question_num, "question")

    user = (
        update.callback_query.from_user
        if update.callback_query
        else update.effective_user
    )

    logger.info(
        f"Pain question {question_num.upper()} asked",
        extra={
            "event": "question_asked",
            "telegram_user_id": user.id if user else None,
            "state": f"Q{question_num[-1]}",
            "question": question_num,
        },
    )

    # Add question number prefix
    question_num_display = question_num.upper()  # Q1, Q2, Q3
    question_text = f"{question_num_display}: {question}"

    # Check if we have a callback query (from back navigation) or message
    if update.callback_query:
        await update.callback_query.message.reply_text(
            question_text,
            reply_markup=pain_question_keyboard(
                question_num, lang, show_back=show_back
            ),
        )
    else:
        await update.message.reply_text(
            question_text,
            reply_markup=pain_question_keyboard(
                question_num, lang, show_back=show_back
            ),
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

    logger.info(
        f"Pain question {question_num.upper()} answer received",
        extra={
            "event": "answer_received",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": f"Q{question_num[-1]}",
            "question": question_num,
            "answer": answer,
        },
    )

    # Recalculate scores from all answers
    score_calculator = ScoreCalculator(user_data)
    score_calculator.recalculate_scores()

    logger.debug(
        "Scores recalculated after answer",
        extra={
            "event": "score_recalculated",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": f"Q{question_num[-1]}",
            "starter_score": user_data.starter_score,
            "core_score": user_data.core_score,
        },
    )

    # Normal flow: continue to next question
    # Ask next question - readiness is handled differently
    if next_question == "readiness":
        return await ask_readiness(update, context)
    else:
        # Show back button for Q2 and Q3
        show_back = next_question in ["q2", "q3"]
        return await ask_pain_question(
            update, context, next_question, next_state, show_back=show_back
        )


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

    user = (
        update.callback_query.from_user
        if update.callback_query
        else update.effective_user
    )

    logger.info(
        "Readiness question (Q4) asked",
        extra={
            "event": "question_asked",
            "telegram_user_id": user.id if user else None,
            "state": "READINESS",
            "question": "readiness",
        },
    )

    # Add question number prefix (Q4)
    question_text = f"Q4: {question}"

    # Check if we have a callback query or message
    if update.callback_query:
        await update.callback_query.message.reply_text(
            question_text,
            reply_markup=readiness_keyboard(lang, show_back=True),
        )
    else:
        await update.message.reply_text(
            question_text,
            reply_markup=readiness_keyboard(lang, show_back=True),
        )

    return states.READINESS


async def readiness_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle readiness answer and show review screen."""
    query = update.callback_query
    await query.answer()

    # Parse callback data using regex for robust extraction
    answer = parse_readiness_answer(query.data)

    user_data = UserData(context)
    user_data.readiness = answer

    logger.info(
        "Readiness question (Q4) answer received",
        extra={
            "event": "answer_received",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "READINESS",
            "question": "readiness",
            "answer": answer.value,
        },
    )

    # Recalculate scores from all answers
    score_calculator = ScoreCalculator(user_data)
    score_calculator.recalculate_scores()

    logger.debug(
        "Scores recalculated after readiness answer",
        extra={
            "event": "score_recalculated",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "READINESS",
            "starter_score": user_data.starter_score,
            "core_score": user_data.core_score,
        },
    )

    # Calculate recommendation (but don't show it yet - show review first)
    recommendation = score_calculator.calculate_recommendation()
    user_data.recommendation = recommendation.value  # Store as string for compatibility

    logger.debug(
        "Recommendation calculated",
        extra={
            "event": "recommendation_calculated",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "READINESS",
            "recommendation": recommendation.value,
            "starter_score": user_data.starter_score,
            "core_score": user_data.core_score,
        },
    )

    # Show review answers screen
    return await show_review_answers(update, context)


async def show_review_answers(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Show review answers screen before recommendation."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    pain_answers = user_data.pain_answers
    readiness = user_data.readiness

    user = (
        update.callback_query.from_user
        if update.callback_query
        else update.effective_user
    )

    logger.info(
        "Review answers screen shown",
        extra={
            "event": "review_screen_shown",
            "telegram_user_id": user.id if user else None,
            "state": "REVIEW_ANSWERS",
        },
    )

    # Build review text
    review_text = get_text("reviewAnswers", lang)

    # Add Q1 answer
    if pain_answers.get("q1"):
        q1_options = get_nested_text(lang, "painQuestions", "q1", "options")
        q1_answer = q1_options.get(pain_answers["q1"], "")
        review_text += get_text("reviewQ1", lang).format(answer=q1_answer) + "\n"

    # Add Q2 answer
    if pain_answers.get("q2"):
        q2_options = get_nested_text(lang, "painQuestions", "q2", "options")
        q2_answer = q2_options.get(pain_answers["q2"], "")
        review_text += get_text("reviewQ2", lang).format(answer=q2_answer) + "\n"

    # Add Q3 answer
    if pain_answers.get("q3"):
        q3_options = get_nested_text(lang, "painQuestions", "q3", "options")
        q3_answer = q3_options.get(pain_answers["q3"], "")
        review_text += get_text("reviewQ3", lang).format(answer=q3_answer) + "\n"

    # Add Q4 (readiness) answer
    if readiness:
        readiness_options = get_nested_text(lang, "readinessQuestion", "options")
        readiness_answer = readiness_options.get(readiness.value, "")
        review_text += get_text("reviewQ4", lang).format(answer=readiness_answer) + "\n"

    # Send review message
    if update.callback_query:
        await update.callback_query.message.reply_text(
            review_text,
            reply_markup=review_answers_keyboard(lang),
        )
    else:
        await update.message.reply_text(
            review_text,
            reply_markup=review_answers_keyboard(lang),
        )

    return states.REVIEW_ANSWERS


async def proceed_to_recommendation_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle proceed to recommendation from review screen."""
    query = update.callback_query
    await query.answer()

    logger.info(
        "Proceed to recommendation clicked",
        extra={
            "event": "proceed_to_recommendation",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "REVIEW_ANSWERS",
        },
    )

    return await show_recommendation(update, context)


async def diag_back_q1_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle back navigation to Q1."""
    query = update.callback_query
    await query.answer()

    logger.info(
        "Back navigation to Q1",
        extra={
            "event": "back_navigation",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "Q2",
            "target_question": "q1",
        },
    )

    return await ask_pain_question(update, context, "q1", states.Q1, show_back=False)


async def diag_back_q2_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle back navigation to Q2."""
    query = update.callback_query
    await query.answer()

    logger.info(
        "Back navigation to Q2",
        extra={
            "event": "back_navigation",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "Q3",
            "target_question": "q2",
        },
    )

    return await ask_pain_question(update, context, "q2", states.Q2, show_back=True)


async def diag_back_q3_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle back navigation to Q3."""
    query = update.callback_query
    await query.answer()

    logger.info(
        "Back navigation to Q3",
        extra={
            "event": "back_navigation",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "READINESS",
            "target_question": "q3",
        },
    )

    return await ask_pain_question(update, context, "q3", states.Q3, show_back=True)
