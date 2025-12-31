"""Keyboard builders for ACPF Bot."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.i18n.messages import get_text, get_nested_text


def language_keyboard() -> InlineKeyboardMarkup:
    """Build language selection keyboard."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇨🇳 中文", callback_data="lang_zh")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
    ])


def start_diagnosis_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build start diagnosis button."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            get_text("startDiagnosis", lang),
            callback_data="start_diagnosis"
        )],
    ])


def pain_question_keyboard(question_num: str, lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for pain point questions (q1, q2, q3)."""
    options = get_nested_text(lang, "painQuestions", question_num, "options")
    
    buttons = []
    for key in ["a", "b", "c", "d"]:
        if key in options:
            buttons.append([
                InlineKeyboardButton(
                    f"{key.upper()}. {options[key]}",
                    callback_data=f"pain_{question_num}_{key}"
                )
            ])
    
    return InlineKeyboardMarkup(buttons)


def readiness_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for readiness question."""
    options = get_nested_text(lang, "readinessQuestion", "options")
    
    buttons = []
    for key in ["a", "b", "c", "d"]:
        if key in options:
            buttons.append([
                InlineKeyboardButton(
                    f"{key.upper()}. {options[key]}",
                    callback_data=f"readiness_{key}"
                )
            ])
    
    return InlineKeyboardMarkup(buttons)


def starter_recommendation_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for Starter recommendation."""
    rec = get_nested_text(lang, "recommendStarter")
    
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(rec.get("cta", "Register Starter"), callback_data="select_starter")],
        [InlineKeyboardButton(rec.get("upsell", "Apply for Core Review"), callback_data="apply_core_review")],
    ])


def core_recommendation_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for Core recommendation."""
    rec = get_nested_text(lang, "recommendCore")
    
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(rec.get("cta", "Register Core"), callback_data="select_core")],
    ])


def gate_question_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for gate question (attended Starter before?)."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_text("gateYes", lang), callback_data="gate_yes")],
        [InlineKeyboardButton(get_text("gateNo", lang), callback_data="gate_no")],
    ])


def gate_rejection_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for gate rejection (redirect to Starter)."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_text("registerStarter", lang), callback_data="register_starter_fallback")],
    ])


def upsell_team_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for upsell question 1 (has team?)."""
    q = get_nested_text(lang, "upsellQuestions", "q1")
    
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(q.get("yes", "Yes"), callback_data="upsell_team_yes")],
        [InlineKeyboardButton(q.get("no", "No"), callback_data="upsell_team_no")],
    ])


def upsell_intent_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for upsell question 2 (scale or foundation?)."""
    q = get_nested_text(lang, "upsellQuestions", "q2")
    
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(q.get("scale", "Scale"), callback_data="upsell_intent_scale")],
        [InlineKeyboardButton(q.get("foundation", "Foundation"), callback_data="upsell_intent_foundation")],
    ])


def upsell_rejected_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for upsell rejection (back to Starter)."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_text("backToStarter", lang), callback_data="select_starter")],
    ])


def confirmation_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for form confirmation."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_text("confirm", lang), callback_data="confirm_submit")],
        [InlineKeyboardButton(get_text("edit", lang), callback_data="edit_form")],
    ])

