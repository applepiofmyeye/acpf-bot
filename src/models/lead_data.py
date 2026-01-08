"""Lead data model for Google Sheets submission."""

from datetime import datetime
from pydantic import BaseModel, Field

from src.enums import Language, CurrentStage, TierInterested, Source


class LeadData(BaseModel):
    """Lead data for Google Sheets submission."""

    timestamp: datetime = Field(default_factory=datetime.now)
    language: Language
    telegram_user_id: str
    telegram_username: str = ""
    full_name: str
    phone: str
    email: str = ""
    business_type: str
    current_stage: CurrentStage | str = ""
    tier_interested: TierInterested | str
    pain_point: str
    source: Source = Source.BOT

    def to_row(self) -> list[str]:
        """Convert to Google Sheets row format.

        Returns:
            List of 12 string values matching the Google Sheets column order:
            1. Timestamp
            2. Language
            3. Telegram User ID
            4. Telegram Username
            5. Full Name
            6. Phone (WhatsApp)
            7. Email
            8. Beauty Business Type
            9. Current Stage (Exploring / Stuck / Scaling)
            10. Tier Interested (Entry / Core / Premium)
            11. Reason for Joining
            12. Source (Bot / Landing Page / Referral)
        """
        return [
            self.timestamp.isoformat(),
            str(self.language),
            self.telegram_user_id,
            self.telegram_username,
            self.full_name,
            self.phone,
            self.email,
            self.business_type,
            str(self.current_stage)
            if isinstance(self.current_stage, CurrentStage)
            else self.current_stage,
            str(self.tier_interested)
            if isinstance(self.tier_interested, TierInterested)
            else self.tier_interested,
            self.pain_point,
            str(self.source),
        ]
