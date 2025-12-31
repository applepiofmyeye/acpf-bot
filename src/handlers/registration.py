"""Registration form handlers for ACPF Bot."""

import re
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.config import PROGRAM_LABELS, PROGRAM_PRICES, ADMIN_CHAT_ID
from src.i18n.messages import get_text, get_nested_text, build_pain_point_summary
from src.keyboards.buttons import confirmation_keyboard
from src.handlers.start import REG_NAME, REG_PHONE, REG_EMAIL, REG_BUSINESS, CONFIRMATION

# Email regex pattern
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Phone regex pattern (digits, spaces, dashes, plus sign, at least 8 digits)
PHONE_PATTERN = re.compile(r'^[\d\s\-\+\(\)]{8,}$')


async def start_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the registration form - ask for name."""
    lang = context.user_data.get("lang", "en")
    
    # Reset form data
    context.user_data["form_data"] = {
        "full_name": None,
        "phone": None,
        "email": None,
        "business_type": None,
    }
    
    form_text = get_nested_text(lang, "form")
    await update.callback_query.message.reply_text(form_text.get("askName", "Please enter your full name:"))
    
    return REG_NAME


async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle name input."""
    lang = context.user_data.get("lang", "en")
    text = update.message.text.strip()
    
    # Validate name (at least 2 characters)
    if len(text) < 2:
        form_text = get_nested_text(lang, "form")
        await update.message.reply_text(form_text.get("invalidName", "Please enter a valid name."))
        return REG_NAME
    
    context.user_data["form_data"]["full_name"] = text
    
    # Ask for phone
    form_text = get_nested_text(lang, "form")
    await update.message.reply_text(form_text.get("askPhone", "Please enter your phone number:"))
    
    return REG_PHONE


async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle phone input."""
    lang = context.user_data.get("lang", "en")
    text = update.message.text.strip()
    
    # Remove common formatting characters for digit count check
    digits_only = re.sub(r'[^\d]', '', text)
    
    # Validate phone: must have at least 8 digits and match pattern
    if len(digits_only) < 8 or not PHONE_PATTERN.match(text):
        form_text = get_nested_text(lang, "form")
        await update.message.reply_text(form_text.get("invalidPhone", "Please enter a valid phone number."))
        return REG_PHONE
    
    context.user_data["form_data"]["phone"] = text
    
    # Ask for email
    form_text = get_nested_text(lang, "form")
    await update.message.reply_text(form_text.get("askEmail", "Please enter your email:"))
    
    return REG_EMAIL


async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle email input."""
    lang = context.user_data.get("lang", "en")
    text = update.message.text.strip()
    form_text = get_nested_text(lang, "form")
    
    # Allow skip
    if text.lower() == "skip":
        context.user_data["form_data"]["email"] = ""
        # Ask for business type
        await update.message.reply_text(form_text.get("askBusinessType", "What type of beauty business are you in?"))
        return REG_BUSINESS
    
    # Validate email format
    if not EMAIL_PATTERN.match(text):
        await update.message.reply_text(form_text.get("invalidEmail", "Please enter a valid email address."))
        return REG_EMAIL
    
    context.user_data["form_data"]["email"] = text
    
    # Ask for business type
    await update.message.reply_text(form_text.get("askBusinessType", "What type of beauty business are you in?"))
    
    return REG_BUSINESS


async def handle_business_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle business type input."""
    lang = context.user_data.get("lang", "en")
    text = update.message.text.strip()
    
    # Validate business type (at least 2 characters)
    if len(text) < 2:
        form_text = get_nested_text(lang, "form")
        await update.message.reply_text(form_text.get("invalidBusinessType", "Please enter a valid business type."))
        return REG_BUSINESS
    
    context.user_data["form_data"]["business_type"] = text
    
    # Show summary
    return await show_summary(update, context)


async def show_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show form summary for confirmation."""
    lang = context.user_data.get("lang", "en")
    form_data = context.user_data["form_data"]
    program = context.user_data.get("program", "starter")
    pain_answers = context.user_data.get("pain_answers", {})
    
    program_label = PROGRAM_LABELS.get(program, program)
    pain_point = build_pain_point_summary(pain_answers, lang)
    
    summary_template = get_text("summary", lang)
    summary_text = summary_template.format(
        name=form_data["full_name"],
        phone=form_data["phone"],
        email=form_data["email"] or "-",
        businessType=form_data["business_type"],
        program=program_label,
        painPoint=pain_point,
    )
    
    await update.message.reply_text(
        summary_text,
        reply_markup=confirmation_keyboard(lang),
    )
    
    return CONFIRMATION


async def confirm_submit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
    """Submit lead to Google Sheets and notify admin."""
    lang = context.user_data.get("lang", "en")
    user = update.callback_query.from_user
    form_data = context.user_data["form_data"]
    program = context.user_data.get("program", "starter")
    track = context.user_data.get("track", "starter")
    pain_answers = context.user_data.get("pain_answers", {})
    
    program_label = PROGRAM_LABELS.get(program, program)
    track_label = "CoreReview" if track == "coreReview" else PROGRAM_LABELS.get(track, track)
    pain_point = build_pain_point_summary(pain_answers, lang)
    
    # Prepare row data for Google Sheets
    row_data = [
        datetime.now().isoformat(),  # Timestamp
        "中文" if lang == "zh" else "English",  # Language
        str(user.id),  # Telegram User ID
        user.username or "",  # Telegram Username
        form_data["full_name"],  # Full Name
        form_data["phone"],  # Phone
        form_data["email"] or "",  # Email
        form_data["business_type"],  # Business Type
        track_label,  # Track
        program_label,  # Program Selected
        pain_point,  # Key Pain Point
        "Telegram Bot",  # Source
    ]
    
    # Lead info for admin notification
    lead_info = f"""📋 New Lead

Program: {program_label}
Track: {track_label}
Name: {form_data["full_name"]}
Phone: {form_data["phone"]}
Email: {form_data["email"] or "-"}
Business Type: {form_data["business_type"]}
Key Pain Point: {pain_point}
Telegram: @{user.username or "N/A"} (ID: {user.id})
Language: {"中文" if lang == "zh" else "English"}
Timestamp: {datetime.now().isoformat()}"""
    
    try:
        # Import and call Google Sheets service
        from src.services.sheets import append_lead_row
        await append_lead_row(row_data)
        
        # Get the correct price based on program
        amount = PROGRAM_PRICES.get(program, "588")
        
        # Send success message with payment info
        success_message = get_text("success", lang).format(amount=amount)
        await update.callback_query.message.reply_text(success_message)
        
        # Notify admin
        if ADMIN_CHAT_ID:
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=f"✅ Lead submitted\n\n{lead_info}",
                )
            except Exception as e:
                print(f"Failed to notify admin: {e}")
        
    except Exception as e:
        print(f"Google Sheets error: {e}")
        
        # Send error message
        await update.callback_query.message.reply_text(get_text("error", lang))
        
        # Notify admin about error
        if ADMIN_CHAT_ID:
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=f"❌ Lead submission error\n\nError: {e}\n\n{lead_info}",
                )
            except Exception as admin_err:
                print(f"Failed to notify admin about error: {admin_err}")
    
    return ConversationHandler.END

