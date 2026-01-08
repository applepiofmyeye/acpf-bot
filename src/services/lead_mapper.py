"""Lead data mapping service for Google Sheets."""

from src.enums import ProgramType, Language, TierInterested
from src.models.lead_data import LeadData
from src.models.form_data import FormData
from src.models.user_data import UserData
from src.i18n.messages import build_pain_point_summary


class LeadMapper:
    """Maps user data to LeadData model for Google Sheets submission."""

    @staticmethod
    def map_to_lead_data(
        user_data: UserData,
        telegram_user_id: int,
        telegram_username: str | None,
        form_data: FormData,
    ) -> LeadData:
        """Map user data to LeadData model.

        Args:
            user_data: UserData instance with user's session data
            telegram_user_id: Telegram user ID
            telegram_username: Telegram username (can be None)
            form_data: FormData model instance

        Returns:
            LeadData instance ready for Google Sheets submission
        """
        lang_code = user_data.lang or "en"
        language = Language.from_code(lang_code)

        program_str = user_data.program or ProgramType.STARTER.value
        program = ProgramType(program_str)

        # Get readiness answer and map to current stage
        readiness = user_data.readiness
        if readiness:
            current_stage = readiness.to_current_stage()
        else:
            current_stage = ""  # Empty string for missing readiness

        # Map program to Tier Interested
        tier_interested = TierInterested.from_program(program)

        # Build pain point summary
        pain_answers = user_data.pain_answers
        pain_point = build_pain_point_summary(pain_answers, lang_code)

        # Create LeadData - Pydantic handles defaults
        return LeadData(
            language=language,
            telegram_user_id=str(telegram_user_id),
            telegram_username=telegram_username or "",
            full_name=form_data.full_name,
            phone=form_data.phone,
            email=form_data.email or "",
            business_type=form_data.business_type,
            current_stage=current_stage,
            tier_interested=tier_interested,
            pain_point=pain_point,
        )
