"""Upsell answers model."""

from pydantic import BaseModel, field_validator

from src.enums import UpsellIntent


class UpsellAnswers(BaseModel):
    """Upsell question answers."""

    has_team: bool | None = None
    intent: UpsellIntent | None = None

    @field_validator("intent", mode="before")
    @classmethod
    def validate_intent(cls, v) -> UpsellIntent | None:
        """Convert string intent to UpsellIntent enum."""
        if v is None:
            return None
        if isinstance(v, UpsellIntent):
            return v
        if isinstance(v, str) and v in ["scale", "foundation"]:
            return UpsellIntent(v)
        return None

    def to_dict(self) -> dict[str, str | bool | None]:
        """Convert to dict format for compatibility."""
        return {
            "has_team": self.has_team,
            "intent": self.intent.value if self.intent else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | bool | None]) -> "UpsellAnswers":
        """Create from dict format."""
        return cls(
            has_team=data.get("has_team"),
            intent=data.get("intent"),
        )
