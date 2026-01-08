"""Pain point answers model."""

from pydantic import BaseModel, field_validator

from src.enums import PainAnswer


class PainAnswers(BaseModel):
    """Pain point question answers."""

    q1: PainAnswer | None = None
    q2: PainAnswer | None = None
    q3: PainAnswer | None = None

    @field_validator("q1", "q2", "q3", mode="before")
    @classmethod
    def validate_answer(cls, v) -> PainAnswer | None:
        """Convert string answer to PainAnswer enum."""
        if v is None:
            return None
        if isinstance(v, PainAnswer):
            return v
        if isinstance(v, str) and v in ["a", "b", "c", "d"]:
            return PainAnswer(v)
        return None

    def to_dict(self) -> dict[str, str | None]:
        """Convert to dict format for compatibility."""
        return {
            "q1": self.q1.value if self.q1 else None,
            "q2": self.q2.value if self.q2 else None,
            "q3": self.q3.value if self.q3 else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | None]) -> "PainAnswers":
        """Create from dict format."""
        return cls(
            q1=data.get("q1"),
            q2=data.get("q2"),
            q3=data.get("q3"),
        )
