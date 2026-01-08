"""Upsell qualification service."""

from src.models.user_data import UserData
from src.services.logging_config import get_logger

logger = get_logger(__name__)


class UpsellQualifier:
    """Determines if user qualifies for Core Review upsell."""

    @staticmethod
    def qualifies_for_core_review(user_data: UserData) -> bool:
        """Check if user qualifies for Core Review.

        Qualification criteria:
        - User must have a team (has_team == True)
        - User must want to scale (intent == "scale")

        Args:
            user_data: UserData instance with user's session data

        Returns:
            True if user qualifies, False otherwise
        """
        upsell_answers = user_data.upsell_answers

        has_team = upsell_answers.get("has_team")
        intent = upsell_answers.get("intent")

        qualifies = has_team is True and intent == "scale"

        logger.debug(
            "Upsell qualification check",
            extra={
                "event": "upsell_qualification_check",
                "has_team": has_team,
                "intent": intent,
                "qualifies": qualifies,
            },
        )

        return qualifies
