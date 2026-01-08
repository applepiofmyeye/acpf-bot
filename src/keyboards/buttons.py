"""Keyboard builders for ACPF Bot."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.i18n.messages import get_text, get_nested_text


def language_keyboard() -> InlineKeyboardMarkup:
    """Build language selection keyboard."""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🇨🇳 中文", callback_data="lang_zh")],
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        ]
    )


def start_diagnosis_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build start diagnosis button."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text("startDiagnosis", lang), callback_data="start_diagnosis"
                )
            ],
        ]
    )


def pain_question_keyboard(
    question_num: str, lang: str, show_back: bool = False
) -> InlineKeyboardMarkup:
    """Build keyboard for pain point questions (q1, q2, q3).

    Args:
        question_num: Question number (q1, q2, q3)
        lang: Language code
        show_back: Whether to show back button (True for Q2, Q3)
    """
    options = get_nested_text(lang, "painQuestions", question_num, "options")

    buttons = []
    for key in ["a", "b", "c", "d"]:
        if key in options:
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"{key.upper()}. {options[key]}",
                        callback_data=f"pain_{question_num}_{key}",
                    )
                ]
            )

    # Add back button for Q2 and Q3
    if show_back:
        prev_question = f"q{int(question_num[1]) - 1}"
        buttons.append(
            [
                InlineKeyboardButton(
                    get_text("back", lang),
                    callback_data=f"diag_back_{prev_question}",
                )
            ]
        )

    return InlineKeyboardMarkup(buttons)


def readiness_keyboard(lang: str, show_back: bool = True) -> InlineKeyboardMarkup:
    """Build keyboard for readiness question.

    Args:
        lang: Language code
        show_back: Whether to show back button (default True)
    """
    options = get_nested_text(lang, "readinessQuestion", "options")

    buttons = []
    for key in ["a", "b", "c", "d"]:
        if key in options:
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"{key.upper()}. {options[key]}",
                        callback_data=f"readiness_{key}",
                    )
                ]
            )

    # Add back button
    if show_back:
        buttons.append(
            [
                InlineKeyboardButton(
                    get_text("back", lang),
                    callback_data="diag_back_q3",
                )
            ]
        )

    return InlineKeyboardMarkup(buttons)


def starter_recommendation_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for Starter recommendation."""
    rec = get_nested_text(lang, "recommendStarter")

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    rec.get("cta", "Register Starter"), callback_data="select_starter"
                )
            ],
            [
                InlineKeyboardButton(
                    rec.get("upsell", "Apply for Core Review"),
                    callback_data="apply_core_review",
                )
            ],
        ]
    )


def core_recommendation_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for Core recommendation."""
    rec = get_nested_text(lang, "recommendCore")

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    rec.get("cta", "Register Core"), callback_data="select_core"
                )
            ],
        ]
    )


def gate_question_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for gate question (attended Starter before?)."""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(get_text("gateYes", lang), callback_data="gate_yes")],
            [InlineKeyboardButton(get_text("gateNo", lang), callback_data="gate_no")],
        ]
    )


def gate_rejection_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for gate rejection (redirect to Starter)."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text("registerStarter", lang),
                    callback_data="register_starter_fallback",
                )
            ],
        ]
    )


def upsell_team_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for upsell question 1 (has team?)."""
    q = get_nested_text(lang, "upsellQuestions", "q1")

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    q.get("yes", "Yes"), callback_data="upsell_team_yes"
                )
            ],
            [InlineKeyboardButton(q.get("no", "No"), callback_data="upsell_team_no")],
        ]
    )


def upsell_intent_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for upsell question 2 (scale or foundation?)."""
    q = get_nested_text(lang, "upsellQuestions", "q2")

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    q.get("scale", "Scale"), callback_data="upsell_intent_scale"
                )
            ],
            [
                InlineKeyboardButton(
                    q.get("foundation", "Foundation"),
                    callback_data="upsell_intent_foundation",
                )
            ],
        ]
    )


def upsell_rejected_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for upsell rejection (back to Starter)."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text("backToStarter", lang), callback_data="select_starter"
                )
            ],
        ]
    )


def confirmation_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for form confirmation."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text("confirm", lang), callback_data="confirm_submit"
                )
            ],
            [
                InlineKeyboardButton(
                    get_text("edit", lang), callback_data="edit_form_menu"
                )
            ],
        ]
    )


def edit_form_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for edit form menu (field selection)."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text("editName", lang), callback_data="edit_field_name"
                )
            ],
            [
                InlineKeyboardButton(
                    get_text("editPhone", lang), callback_data="edit_field_phone"
                )
            ],
            [
                InlineKeyboardButton(
                    get_text("editEmail", lang), callback_data="edit_field_email"
                )
            ],
            [
                InlineKeyboardButton(
                    get_text("editBusiness", lang), callback_data="edit_field_business"
                )
            ],
            [
                InlineKeyboardButton(
                    get_text("back", lang), callback_data="back_to_summary"
                )
            ],
        ]
    )


def registration_back_keyboard(
    lang: str, current_field: str
) -> InlineKeyboardMarkup | None:
    """Build keyboard with back button for registration fields.

    Args:
        lang: Language code
        current_field: Current field name (full_name, phone, email, business_type)

    Returns:
        Keyboard with back button, or None if no back button needed (first field)
    """
    if current_field == "full_name":
        return None  # No back button on first field

    buttons = []
    if current_field == "phone":
        buttons.append(
            [
                InlineKeyboardButton(
                    get_text("back", lang), callback_data="reg_back_name"
                )
            ]
        )
    elif current_field == "email":
        buttons.append(
            [
                InlineKeyboardButton(
                    get_text("back", lang), callback_data="reg_back_phone"
                )
            ]
        )
    elif current_field == "business_type":
        buttons.append(
            [
                InlineKeyboardButton(
                    get_text("back", lang), callback_data="reg_back_email"
                )
            ]
        )

    return InlineKeyboardMarkup(buttons) if buttons else None


def review_answers_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for review answers screen."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text("proceedToRecommendation", lang),
                    callback_data="proceed_to_recommendation",
                )
            ],
            [
                InlineKeyboardButton(
                    f"{get_text('editAnswer', lang)} - Q1",
                    callback_data="review_edit_q1",
                )
            ],
            [
                InlineKeyboardButton(
                    f"{get_text('editAnswer', lang)} - Q2",
                    callback_data="review_edit_q2",
                )
            ],
            [
                InlineKeyboardButton(
                    f"{get_text('editAnswer', lang)} - Q3",
                    callback_data="review_edit_q3",
                )
            ],
            [
                InlineKeyboardButton(
                    f"{get_text('editAnswer', lang)} - Q4",
                    callback_data="review_edit_readiness",
                )
            ],
        ]
    )
