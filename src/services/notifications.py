"""Admin notification service for ACPF Bot.

DEPRECATED: This module is deprecated and notification calls have been removed
from the handlers. The functions remain for potential future use but are not
currently called anywhere in the codebase.
"""

import warnings
from telegram import Bot

from src.config import ADMIN_CHAT_ID
from src.services.logging_config import get_logger

logger = get_logger(__name__)


def _normalize_admin_chat_id(chat_id: str | None) -> str | None:
    """Normalize admin chat ID by stripping whitespace.

    Args:
        chat_id: Raw chat ID from config (may have whitespace or @ prefix)

    Returns:
        Normalized chat ID string or None if invalid
    """
    if not chat_id:
        return None

    # Strip whitespace
    normalized = chat_id.strip()

    # Handle @username format (Telegram supports this for public channels/groups)
    # For now, we'll pass it through as-is since Telegram API handles it
    if normalized.startswith("@"):
        return normalized

    # If it's numeric, ensure it's clean
    if normalized.replace("-", "").replace("+", "").isdigit():
        return normalized

    # If it's not numeric and doesn't start with @, might be invalid
    # But we'll still try to send it (could be a channel username without @)
    return normalized if normalized else None


async def notify_admin(bot: Bot, message: str) -> bool:
    """Send a notification message to the admin.

    DEPRECATED: This function is deprecated and not currently used.

    Args:
        bot: The Telegram bot instance
        message: The message to send

    Returns:
        True if notification was sent successfully, False otherwise
    """
    warnings.warn(
        "notify_admin is deprecated and not currently used",
        DeprecationWarning,
        stacklevel=2,
    )
    admin_chat_id = _normalize_admin_chat_id(ADMIN_CHAT_ID)

    if not admin_chat_id:
        logger.info(
            "ADMIN_CHAT_ID not set, skipping notification",
            extra={"event": "notification_skipped"},
        )
        return False

    try:
        await bot.send_message(
            chat_id=admin_chat_id,
            text=message,
        )
        logger.info(
            "Admin notification sent successfully",
            extra={"event": "notification_sent", "chat_id": admin_chat_id[:10] + "..."},
        )
        return True
    except Exception:
        logger.exception(
            "Failed to send admin notification",
            extra={
                "event": "notification_failed",
                "chat_id": admin_chat_id[:10] + "...",
            },
        )
        return False


async def notify_new_lead(
    bot: Bot,
    program: str,
    track: str,
    name: str,
    phone: str,
    email: str,
    business_type: str,
    pain_point: str,
    username: str,
    user_id: int,
    language: str,
    timestamp: str,
) -> bool:
    """Notify admin about a new lead registration.

    DEPRECATED: This function is deprecated and not currently used.

    Args:
        bot: The Telegram bot instance
        program: Selected program (Starter/Professional Certificate Beauty Management Strategy)
        track: Track (Starter/Professional Certificate Beauty Management Strategy/CoreReview)
        name: User's full name
        phone: User's phone number
        email: User's email
        business_type: User's beauty business type
        pain_point: Key pain point summary
        username: Telegram username
        user_id: Telegram user ID
        language: Selected language
        timestamp: Registration timestamp

    Returns:
        True if notification was sent successfully, False otherwise
    """
    message = f"""✅ New Lead Registered

📦 Program: {program}
🏷️ Track: {track}

👤 Name: {name}
📱 Phone: {phone}
📧 Email: {email or "-"}
💼 Business Type: {business_type}

🎯 Key Pain Point: {pain_point}

📱 Telegram: @{username or "N/A"} (ID: {user_id})
🌐 Language: {language}
🕐 Time: {timestamp}"""

    return await notify_admin(bot, message)


async def notify_core_review_request(
    bot: Bot,
    username: str,
    user_id: int,
    language: str,
) -> bool:
    """Notify admin about a Professional Certificate Beauty Management Strategy review request (upsell flow start).

    DEPRECATED: This function is deprecated and not currently used.

    Args:
        bot: The Telegram bot instance
        username: Telegram username
        user_id: Telegram user ID
        language: Selected language

    Returns:
        True if notification was sent successfully, False otherwise
    """
    message = f"""🔔 Professional Certificate Beauty Management Strategy Review Request

👤 User: @{username or "N/A"} (ID: {user_id})
🌐 Language: {language}
📊 Status: Started upsell flow"""

    return await notify_admin(bot, message)


async def notify_core_review_qualified(
    bot: Bot,
    username: str,
    user_id: int,
    has_team: bool,
    intent: str,
) -> bool:
    """Notify admin about a Professional Certificate Beauty Management Strategy review qualification.

    DEPRECATED: This function is deprecated and not currently used.

    Args:
        bot: The Telegram bot instance
        username: Telegram username
        user_id: Telegram user ID
        has_team: Whether user has a team
        intent: User's intent (scale/foundation)

    Returns:
        True if notification was sent successfully, False otherwise
    """
    message = f"""✅ Professional Certificate Beauty Management Strategy Review Qualified

👤 User: @{username or "N/A"} (ID: {user_id})
👥 Has Team: {"Yes" if has_team else "No"}
🎯 Intent: {intent.title()}
📊 Status: Approved for Professional Certificate Beauty Management Strategy review"""

    return await notify_admin(bot, message)


async def notify_submission_error(
    bot: Bot,
    error: str,
    lead_info: str,
) -> bool:
    """Notify admin about a submission error.

    DEPRECATED: This function is deprecated and not currently used.

    Args:
        bot: The Telegram bot instance
        error: Error message
        lead_info: Lead information that failed to submit

    Returns:
        True if notification was sent successfully, False otherwise
    """
    message = f"""❌ Lead Submission Error

⚠️ Error: {error}

{lead_info}"""

    return await notify_admin(bot, message)
