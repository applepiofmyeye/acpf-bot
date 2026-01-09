"""Enums for ACPF Bot."""

from enum import Enum


class ProgramType(str, Enum):
    """Program types available in the system."""

    STARTER = "starter"
    CORE = "Professional Certificate Beauty Management Strategy"
    CORE_REVIEW = "coreReview"

    def __str__(self) -> str:
        """Return the string value for compatibility."""
        return self.value


class ScoreType(str, Enum):
    """Score types for recommendation calculation."""

    STARTER = "starter"
    CORE = "Professional Certificate Beauty Management Strategy"

    def __str__(self) -> str:
        """Return the string value for compatibility."""
        return self.value


class Language(str, Enum):
    """Language options for the bot."""

    CHINESE = "中文"
    ENGLISH = "English"

    @classmethod
    def from_code(cls, code: str) -> "Language":
        """Convert language code (zh/en) to Language enum."""
        mapping = {"zh": cls.CHINESE, "en": cls.ENGLISH}
        return mapping.get(code, cls.ENGLISH)

    def to_code(self) -> str:
        """Convert Language enum to code (zh/en)."""
        mapping = {Language.CHINESE: "zh", Language.ENGLISH: "en"}
        return mapping.get(self, "en")

    def __str__(self) -> str:
        """Return the string value for compatibility."""
        return self.value


class CurrentStage(str, Enum):
    """Current business stage based on readiness answer."""

    EXPLORING = "Exploring"
    STUCK = "Stuck"
    SCALING = "Scaling"

    @classmethod
    def from_readiness(cls, readiness: "ReadinessAnswer | str") -> "CurrentStage | str":
        """Map readiness answer to current stage.

        Args:
            readiness: ReadinessAnswer enum or string (a, b, c, d)

        Returns:
            CurrentStage enum or empty string if invalid

        Note:
            Prefer using ReadinessAnswer.to_current_stage() for type-safe mapping.
            This method is kept for backward compatibility.
        """
        # Handle enum input
        if isinstance(readiness, ReadinessAnswer):
            return readiness.to_current_stage()

        # Handle string input (backward compatibility)
        if isinstance(readiness, str):
            try:
                readiness_enum = ReadinessAnswer(readiness)
                return readiness_enum.to_current_stage()
            except ValueError:
                return ""

        return ""

    def __str__(self) -> str:
        """Return the string value for compatibility."""
        return self.value


class TierInterested(str, Enum):
    """Tier interested based on program selection."""

    ENTRY = "Entry"
    CORE = "Professional Certificate Beauty Management Strategy"
    PREMIUM = "Premium"

    @classmethod
    def from_program(cls, program: ProgramType) -> "TierInterested":
        """Map program type to tier interested.

        Args:
            program: ProgramType enum

        Returns:
            TierInterested enum
        """
        mapping = {
            ProgramType.STARTER: cls.ENTRY,
            ProgramType.CORE: cls.CORE,
            ProgramType.CORE_REVIEW: cls.PREMIUM,
        }
        return mapping.get(program, cls.ENTRY)

    def __str__(self) -> str:
        """Return the string value for compatibility."""
        return self.value


class Source(str, Enum):
    """Lead source."""

    BOT = "Bot"
    LANDING_PAGE = "Landing Page"
    REFERRAL = "Referral"

    def __str__(self) -> str:
        """Return the string value for compatibility."""
        return self.value


class ReadinessAnswer(str, Enum):
    """Readiness question answer options."""

    A = "a"
    B = "b"
    C = "c"
    D = "d"

    def to_current_stage(self) -> "CurrentStage":
        """Map readiness answer to current business stage.

        Semantic mapping:
        - A: "Just exploring, not ready" -> EXPLORING
        - B: "Willing to learn if direction is right" -> EXPLORING
        - C: "Already looking for methods, ready to act" -> STUCK
        - D: "Clearly understands problem, needs systematic solution" -> SCALING

        Returns:
            CurrentStage enum corresponding to this readiness answer
        """
        mapping = {
            ReadinessAnswer.A: CurrentStage.EXPLORING,
            ReadinessAnswer.B: CurrentStage.EXPLORING,
            ReadinessAnswer.C: CurrentStage.STUCK,
            ReadinessAnswer.D: CurrentStage.SCALING,
        }
        return mapping[self]

    def __str__(self) -> str:
        """Return the string value for compatibility."""
        return self.value


class PainAnswer(str, Enum):
    """Pain point question answer options."""

    A = "a"
    B = "b"
    C = "c"
    D = "d"

    def __str__(self) -> str:
        """Return the string value for compatibility."""
        return self.value


class UpsellIntent(str, Enum):
    """Upsell intent options."""

    SCALE = "scale"
    FOUNDATION = "foundation"

    def __str__(self) -> str:
        """Return the string value for compatibility."""
        return self.value
