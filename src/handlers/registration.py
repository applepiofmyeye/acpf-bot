"""Registration form handlers for ACPF Bot."""

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


from src.constants import PROGRAM_LABELS
from src.enums import ProgramType
from src.i18n.messages import get_text, get_nested_text, build_pain_point_summary
from src.keyboards.buttons import (
    confirmation_keyboard,
    edit_form_menu_keyboard,
    registration_back_keyboard,
)
from src import states
from src.models.user_data import UserData
from src.models.form_data import FormData
from src.services.validation import FormValidator
from src.services.lead_mapper import LeadMapper
from src.services.sheets import append_lead_row
from src.services.logging_config import get_logger

logger = get_logger(__name__)


async def start_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the registration form - show disclaimer and ask for name."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    user = (
        update.callback_query.from_user
        if update.callback_query
        else update.effective_user
    )

    logger.info(
        "Registration form started",
        extra={
            "event": "form_started",
            "telegram_user_id": user.id if user else None,
            "state": "REG_NAME",
        },
    )

    # Reset form data
    user_data.set_form_data(
        {
            "full_name": None,
            "phone": None,
            "email": None,
            "business_type": None,
        }
    )

    form_text = get_nested_text(lang, "form")

    # Show disclaimer first
    await update.callback_query.message.reply_text(form_text.get("disclaimer", ""))

    # Then ask for name (no back button on first field)
    logger.info(
        "Form field prompt shown",
        extra={
            "event": "form_field_prompt_shown",
            "telegram_user_id": user.id if user else None,
            "state": "REG_NAME",
            "field": "full_name",
        },
    )

    await update.callback_query.message.reply_text(
        form_text.get("askName", "Please enter your full name:"),
        reply_markup=registration_back_keyboard(lang, "full_name"),
    )

    return states.REG_NAME


async def handle_form_field(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    field_name: str,
    current_state: int,
    next_state: int,
    next_prompt_key: str,
) -> int:
    """Generic handler for form field input (DRY principle)."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    text = update.message.text.strip()
    form_text = get_nested_text(lang, "form")
    user = update.effective_user

    logger.info(
        "Form field input received",
        extra={
            "event": "form_field_input_received",
            "telegram_user_id": user.id if user else None,
            "state": f"REG_{field_name.upper()}",
            "field": field_name,
        },
    )

    # Validate field using FormValidator
    validator = FormValidator()

    if field_name == "full_name":
        is_valid, error_msg = validator.validate_name(text)
        error_key = "invalidName"
    elif field_name == "phone":
        is_valid, error_msg = validator.validate_phone(text)
        error_key = "invalidPhone"
    elif field_name == "email":
        is_valid, error_msg = validator.validate_email(text)
        error_key = "invalidEmail"
    elif field_name == "business_type":
        is_valid, error_msg = validator.validate_business_type(text)
        error_key = "invalidBusinessType"
    else:
        is_valid = False
        error_msg = "Invalid field"
        error_key = "invalidBusinessType"

    if not is_valid:
        logger.info(
            "Form field validation failed",
            extra={
                "event": "form_field_validation_failed",
                "telegram_user_id": user.id if user else None,
                "state": f"REG_{field_name.upper()}",
                "field": field_name,
                "validation_result": "failure",
                "error": error_msg,
            },
        )
        await update.message.reply_text(form_text.get(error_key, error_msg))
        return current_state

    # Update form data using update_form_field helper
    user_data.update_form_field(field_name, text)

    logger.info(
        "Form field validated successfully",
        extra={
            "event": "form_field_validated",
            "telegram_user_id": user.id if user else None,
            "state": f"REG_{field_name.upper()}",
            "field": field_name,
            "validation_result": "success",
        },
    )

    # Ask for next field with back button
    back_keyboard = registration_back_keyboard(lang, field_name)
    logger.info(
        "Form field prompt shown",
        extra={
            "event": "form_field_prompt_shown",
            "telegram_user_id": user.id if user else None,
            "state": f"REG_{next_prompt_key.replace('ask', '').upper()}",
            "field": next_prompt_key.replace("ask", "").lower(),
        },
    )
    await update.message.reply_text(
        form_text.get(next_prompt_key, ""),
        reply_markup=back_keyboard,
    )

    return next_state


async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle name input."""
    return await handle_form_field(
        update, context, "full_name", states.REG_NAME, states.REG_PHONE, "askPhone"
    )


async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle phone input."""
    return await handle_form_field(
        update, context, "phone", states.REG_PHONE, states.REG_EMAIL, "askEmail"
    )


async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle email input."""
    return await handle_form_field(
        update,
        context,
        "email",
        states.REG_EMAIL,
        states.REG_BUSINESS,
        "askBusinessType",
    )


async def handle_business_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle business type input."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    text = update.message.text.strip()
    form_text = get_nested_text(lang, "form")
    user = update.effective_user

    logger.info(
        "Form field input received",
        extra={
            "event": "form_field_input_received",
            "telegram_user_id": user.id if user else None,
            "state": "REG_BUSINESS",
            "field": "business_type",
        },
    )

    # Validate business type using FormValidator
    validator = FormValidator()
    is_valid, error_msg = validator.validate_business_type(text)

    if not is_valid:
        logger.info(
            "Form field validation failed",
            extra={
                "event": "form_field_validation_failed",
                "telegram_user_id": user.id if user else None,
                "state": "REG_BUSINESS",
                "field": "business_type",
                "validation_result": "failure",
                "error": error_msg,
            },
        )
        await update.message.reply_text(form_text.get("invalidBusinessType", error_msg))
        return states.REG_BUSINESS

    # Update form data
    user_data.update_form_field("business_type", text)

    logger.info(
        "Form field validated successfully",
        extra={
            "event": "form_field_validated",
            "telegram_user_id": user.id if user else None,
            "state": "REG_BUSINESS",
            "field": "business_type",
            "validation_result": "success",
        },
    )

    # Show summary
    return await show_summary(update, context)


async def show_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show form summary for confirmation."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    form_data_model = user_data.get_form_data_model()
    program_str = user_data.program or ProgramType.STARTER.value
    pain_answers = user_data.pain_answers
    user = (
        update.callback_query.from_user
        if update.callback_query
        else update.effective_user
    )

    logger.info(
        "Form summary shown",
        extra={
            "event": "form_summary_shown",
            "telegram_user_id": user.id if user else None,
            "state": "CONFIRMATION",
        },
    )

    program_label = PROGRAM_LABELS.get(ProgramType(program_str), program_str)
    pain_point = build_pain_point_summary(pain_answers, lang)

    # Get form data values, handling None case
    if form_data_model:
        name = form_data_model.full_name
        phone = form_data_model.phone
        email = form_data_model.email or "-"
        business_type = form_data_model.business_type
    else:
        form_data = user_data.form_data
        name = form_data.get("full_name") or ""
        phone = form_data.get("phone") or ""
        email = form_data.get("email") or "-"
        business_type = form_data.get("business_type") or ""

    summary_template = get_text("summary", lang)
    summary_text = summary_template.format(
        name=name,
        phone=phone,
        email=email,
        businessType=business_type,
        program=program_label,
        painPoint=pain_point,
    )

    # Handle both callback_query and message updates
    if update.callback_query:
        await update.callback_query.message.reply_text(
            summary_text,
            reply_markup=confirmation_keyboard(lang),
        )
    else:
        await update.message.reply_text(
            summary_text,
            reply_markup=confirmation_keyboard(lang),
        )

    return states.CONFIRMATION


async def confirm_submit_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle form confirmation - submit to Google Sheets."""
    query = update.callback_query
    await query.answer()

    logger.info(
        "Form submission initiated",
        extra={
            "event": "form_submission_initiated",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "CONFIRMATION",
        },
    )

    return await submit_lead(update, context)


async def edit_form_menu_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle edit form menu - show field selection."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    lang = user_data.lang or "en"

    logger.info(
        "Edit form menu shown",
        extra={
            "event": "edit_form_menu_shown",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "EDIT_FORM_MENU",
        },
    )

    await query.message.reply_text(
        get_text("editMenu", lang),
        reply_markup=edit_form_menu_keyboard(lang),
    )

    return states.EDIT_FORM_MENU


async def edit_field_name_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle edit name field."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    lang = user_data.lang or "en"
    form_text = get_nested_text(lang, "form")

    logger.info(
        "Field edit initiated",
        extra={
            "event": "field_edit_initiated",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "EDIT_NAME",
            "field": "full_name",
        },
    )

    await query.message.reply_text(
        form_text.get("askName", "Please enter your full name:")
    )

    return states.EDIT_NAME


async def edit_field_phone_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle edit phone field."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    lang = user_data.lang or "en"
    form_text = get_nested_text(lang, "form")

    logger.info(
        "Field edit initiated",
        extra={
            "event": "field_edit_initiated",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "EDIT_PHONE",
            "field": "phone",
        },
    )

    await query.message.reply_text(
        form_text.get("askPhone", "Please enter your phone number:")
    )

    return states.EDIT_PHONE


async def edit_field_email_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle edit email field."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    lang = user_data.lang or "en"
    form_text = get_nested_text(lang, "form")

    logger.info(
        "Field edit initiated",
        extra={
            "event": "field_edit_initiated",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "EDIT_EMAIL",
            "field": "email",
        },
    )

    await query.message.reply_text(
        form_text.get("askEmail", "Please enter your email:")
    )

    return states.EDIT_EMAIL


async def edit_field_business_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle edit business type field."""
    query = update.callback_query
    await query.answer()

    user_data = UserData(context)
    lang = user_data.lang or "en"
    form_text = get_nested_text(lang, "form")

    logger.info(
        "Field edit initiated",
        extra={
            "event": "field_edit_initiated",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "EDIT_BUSINESS",
            "field": "business_type",
        },
    )

    await query.message.reply_text(
        form_text.get("askBusinessType", "What type of beauty business are you in?")
    )

    return states.EDIT_BUSINESS


async def back_to_summary_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle back to summary from edit menu."""
    query = update.callback_query
    await query.answer()

    logger.info(
        "Back to summary from edit menu",
        extra={
            "event": "back_navigation",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "EDIT_FORM_MENU",
            "target": "summary",
        },
    )

    return await show_summary(update, context)


async def reg_back_name_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle back to name field."""
    query = update.callback_query
    await query.answer()

    logger.info(
        "Back navigation to name field",
        extra={
            "event": "back_navigation",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "REG_PHONE",
            "target_field": "full_name",
        },
    )

    user_data = UserData(context)
    lang = user_data.lang or "en"
    form_text = get_nested_text(lang, "form")

    # Edit the previous message to show name prompt (no back button on first field)
    await query.message.edit_text(
        form_text.get("askName", "Please enter your full name:"),
        reply_markup=None,
    )

    return states.REG_NAME


async def reg_back_phone_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle back to phone field."""
    query = update.callback_query
    await query.answer()

    logger.info(
        "Back navigation to phone field",
        extra={
            "event": "back_navigation",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "REG_EMAIL",
            "target_field": "phone",
        },
    )

    user_data = UserData(context)
    lang = user_data.lang or "en"
    form_text = get_nested_text(lang, "form")

    # Edit the previous message to show phone prompt with back button
    await query.message.edit_text(
        form_text.get("askPhone", "Please enter your phone number:"),
        reply_markup=registration_back_keyboard(lang, "phone"),
    )

    return states.REG_PHONE


async def reg_back_email_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle back to email field."""
    query = update.callback_query
    await query.answer()

    logger.info(
        "Back navigation to email field",
        extra={
            "event": "back_navigation",
            "telegram_user_id": query.from_user.id if query.from_user else None,
            "state": "REG_BUSINESS",
            "target_field": "email",
        },
    )

    user_data = UserData(context)
    lang = user_data.lang or "en"
    form_text = get_nested_text(lang, "form")

    # Edit the previous message to show email prompt with back button
    await query.message.edit_text(
        form_text.get("askEmail", "Please enter your email:"),
        reply_markup=registration_back_keyboard(lang, "email"),
    )

    return states.REG_EMAIL


async def handle_edit_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle name input from edit field."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    text = update.message.text.strip()
    form_text = get_nested_text(lang, "form")
    user = update.effective_user

    logger.info(
        "Form field input received (edit)",
        extra={
            "event": "form_field_input_received",
            "telegram_user_id": user.id if user else None,
            "state": "EDIT_NAME",
            "field": "full_name",
        },
    )

    # Validate name using FormValidator
    validator = FormValidator()
    is_valid, error_msg = validator.validate_name(text)

    if not is_valid:
        logger.info(
            "Form field validation failed (edit)",
            extra={
                "event": "form_field_validation_failed",
                "telegram_user_id": user.id if user else None,
                "state": "EDIT_NAME",
                "field": "full_name",
                "validation_result": "failure",
                "error": error_msg,
            },
        )
        await update.message.reply_text(form_text.get("invalidName", error_msg))
        return states.EDIT_NAME

    # Update form data
    user_data.update_form_field("full_name", text)

    logger.info(
        "Form field validated successfully (edit)",
        extra={
            "event": "form_field_validated",
            "telegram_user_id": user.id if user else None,
            "state": "EDIT_NAME",
            "field": "full_name",
            "validation_result": "success",
        },
    )

    # Return to summary
    return await show_summary(update, context)


async def handle_edit_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle phone input from edit field."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    text = update.message.text.strip()
    form_text = get_nested_text(lang, "form")
    user = update.effective_user

    logger.info(
        "Form field input received (edit)",
        extra={
            "event": "form_field_input_received",
            "telegram_user_id": user.id if user else None,
            "state": "EDIT_PHONE",
            "field": "phone",
        },
    )

    # Validate phone using FormValidator
    validator = FormValidator()
    is_valid, error_msg = validator.validate_phone(text)

    if not is_valid:
        logger.info(
            "Form field validation failed (edit)",
            extra={
                "event": "form_field_validation_failed",
                "telegram_user_id": user.id if user else None,
                "state": "EDIT_PHONE",
                "field": "phone",
                "validation_result": "failure",
                "error": error_msg,
            },
        )
        await update.message.reply_text(form_text.get("invalidPhone", error_msg))
        return states.EDIT_PHONE

    # Update form data
    user_data.update_form_field("phone", text)

    logger.info(
        "Form field validated successfully (edit)",
        extra={
            "event": "form_field_validated",
            "telegram_user_id": user.id if user else None,
            "state": "EDIT_PHONE",
            "field": "phone",
            "validation_result": "success",
        },
    )

    # Return to summary
    return await show_summary(update, context)


async def handle_edit_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle email input from edit field."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    text = update.message.text.strip()
    form_text = get_nested_text(lang, "form")
    user = update.effective_user

    logger.info(
        "Form field input received (edit)",
        extra={
            "event": "form_field_input_received",
            "telegram_user_id": user.id if user else None,
            "state": "EDIT_EMAIL",
            "field": "email",
        },
    )

    # Validate email using FormValidator
    validator = FormValidator()
    is_valid, error_msg = validator.validate_email(text)

    if not is_valid:
        logger.info(
            "Form field validation failed (edit)",
            extra={
                "event": "form_field_validation_failed",
                "telegram_user_id": user.id if user else None,
                "state": "EDIT_EMAIL",
                "field": "email",
                "validation_result": "failure",
                "error": error_msg,
            },
        )
        await update.message.reply_text(form_text.get("invalidEmail", error_msg))
        return states.EDIT_EMAIL

    # Update form data
    user_data.update_form_field("email", text)

    logger.info(
        "Form field validated successfully (edit)",
        extra={
            "event": "form_field_validated",
            "telegram_user_id": user.id if user else None,
            "state": "EDIT_EMAIL",
            "field": "email",
            "validation_result": "success",
        },
    )

    # Return to summary
    return await show_summary(update, context)


async def handle_edit_business(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle business type input from edit field."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    text = update.message.text.strip()
    form_text = get_nested_text(lang, "form")
    user = update.effective_user

    logger.info(
        "Form field input received (edit)",
        extra={
            "event": "form_field_input_received",
            "telegram_user_id": user.id if user else None,
            "state": "EDIT_BUSINESS",
            "field": "business_type",
        },
    )

    # Validate business type using FormValidator
    validator = FormValidator()
    is_valid, error_msg = validator.validate_business_type(text)

    if not is_valid:
        logger.info(
            "Form field validation failed (edit)",
            extra={
                "event": "form_field_validation_failed",
                "telegram_user_id": user.id if user else None,
                "state": "EDIT_BUSINESS",
                "field": "business_type",
                "validation_result": "failure",
                "error": error_msg,
            },
        )
        await update.message.reply_text(form_text.get("invalidBusinessType", error_msg))
        return states.EDIT_BUSINESS

    # Update form data
    user_data.update_form_field("business_type", text)

    logger.info(
        "Form field validated successfully (edit)",
        extra={
            "event": "form_field_validated",
            "telegram_user_id": user.id if user else None,
            "state": "EDIT_BUSINESS",
            "field": "business_type",
            "validation_result": "success",
        },
    )

    # Return to summary
    return await show_summary(update, context)


async def submit_lead(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Submit lead to Google Sheets."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    user = update.callback_query.from_user
    form_data_model = user_data.get_form_data_model()

    if not form_data_model:
        # Fallback to dict if model not available
        form_data_dict = user_data.form_data
        try:
            form_data_model = FormData(
                full_name=form_data_dict.get("full_name") or "",
                phone=form_data_dict.get("phone") or "",
                email=form_data_dict.get("email"),
                business_type=form_data_dict.get("business_type") or "",
            )
        except Exception:
            await update.callback_query.message.reply_text(get_text("error", lang))
            return ConversationHandler.END

    try:
        # Map user data to LeadData using LeadMapper
        lead_mapper = LeadMapper()
        lead_data = lead_mapper.map_to_lead_data(
            user_data=user_data,
            telegram_user_id=user.id,
            telegram_username=user.username,
            form_data=form_data_model,
        )

        # Submit to Google Sheets
        await append_lead_row(lead_data.to_row())

        logger.info(
            "Lead submitted successfully",
            extra={
                "event": "lead_submitted",
                "telegram_user_id": user.id,
                "state": "CONFIRMATION",
            },
        )

        # Send success message
        await update.callback_query.message.reply_text(get_text("success", lang))

        # Send payment info
        payment_text = get_text("paymentInfo", lang)
        await update.callback_query.message.reply_text(payment_text)

    except Exception:
        logger.exception(
            "Google Sheets submission error",
            extra={
                "event": "lead_submission_error",
                "telegram_user_id": user.id,
                "state": "CONFIRMATION",
            },
        )

        # Send error message
        await update.callback_query.message.reply_text(get_text("error", lang))

    return ConversationHandler.END
