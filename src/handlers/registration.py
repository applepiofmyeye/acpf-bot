"""Registration form handlers for ACPF Bot."""

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.constants import PROGRAM_LABELS
from src.enums import ProgramType
from src.i18n.messages import get_text, get_nested_text, build_pain_point_summary
from src.keyboards.buttons import confirmation_keyboard
from src import states
from src.models.user_data import UserData
from src.models.form_data import FormData
from src.services.validation import FormValidator
from src.services.lead_mapper import LeadMapper
from src.services.sheets import append_lead_row


async def start_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the registration form - show disclaimer and ask for name."""
    user_data = UserData(context)
    lang = user_data.lang or "en"

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

    # Then ask for name
    await update.callback_query.message.reply_text(
        form_text.get("askName", "Please enter your full name:")
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
        await update.message.reply_text(form_text.get(error_key, error_msg))
        return current_state

    # Update form data using update_form_field helper
    user_data.update_form_field(field_name, text)

    # Ask for next field
    await update.message.reply_text(form_text.get(next_prompt_key, ""))

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

    # Validate business type using FormValidator
    validator = FormValidator()
    is_valid, error_msg = validator.validate_business_type(text)

    if not is_valid:
        await update.message.reply_text(form_text.get("invalidBusinessType", error_msg))
        return states.REG_BUSINESS

    # Update form data
    user_data.update_form_field("business_type", text)

    # Show summary
    return await show_summary(update, context)


async def show_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show form summary for confirmation."""
    user_data = UserData(context)
    lang = user_data.lang or "en"
    form_data_model = user_data.get_form_data_model()
    program_str = user_data.program or ProgramType.STARTER.value
    pain_answers = user_data.pain_answers

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

    return await submit_lead(update, context)


async def edit_form_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle edit form - restart form collection."""
    query = update.callback_query
    await query.answer()

    return await start_form(update, context)


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

        # Send success message
        await update.callback_query.message.reply_text(get_text("success", lang))

        # Send payment info
        payment_text = get_text("paymentInfo", lang)
        await update.callback_query.message.reply_text(payment_text)

    except Exception as e:
        print(f"Google Sheets error: {e}")

        # Send error message
        await update.callback_query.message.reply_text(get_text("error", lang))

    return ConversationHandler.END
