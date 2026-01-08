"""Admin notification service for ACPF Bot."""

from telegram import Bot

from src.config import ADMIN_CHAT_ID


async def notify_admin(bot: Bot, message: str) -> bool:
    """Send a notification message to the admin.

    Args:
        bot: The Telegram bot instance
        message: The message to send

    Returns:
        True if notification was sent successfully, False otherwise
    """
    if not ADMIN_CHAT_ID:
        print("ADMIN_CHAT_ID not set, skipping notification")
        return False

    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=message,
        )
        return True
    except Exception as e:
        print(f"Failed to send admin notification: {e}")
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

    Args:
        bot: The Telegram bot instance
        program: Selected program (Starter/Core)
        track: Track (Starter/Core/CoreReview)
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
    """Notify admin about a Core review request (upsell flow start).

    Args:
        bot: The Telegram bot instance
        username: Telegram username
        user_id: Telegram user ID
        language: Selected language

    Returns:
        True if notification was sent successfully, False otherwise
    """
    message = f"""🔔 Core Review Request

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
    """Notify admin about a Core review qualification.

    Args:
        bot: The Telegram bot instance
        username: Telegram username
        user_id: Telegram user ID
        has_team: Whether user has a team
        intent: User's intent (scale/foundation)

    Returns:
        True if notification was sent successfully, False otherwise
    """
    message = f"""✅ Core Review Qualified

👤 User: @{username or "N/A"} (ID: {user_id})
👥 Has Team: {"Yes" if has_team else "No"}
🎯 Intent: {intent.title()}
📊 Status: Approved for Core review"""

    return await notify_admin(bot, message)


async def notify_submission_error(
    bot: Bot,
    error: str,
    lead_info: str,
) -> bool:
    """Notify admin about a submission error.

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
