"""Business constants for ACPF Bot."""

from src.enums import ProgramType, ScoreType

# Scoring rules for recommendation logic
# Default scoring: a -> starter, b/c/d -> core
_DEFAULT_SCORING = {
    "a": ScoreType.STARTER,
    "b": ScoreType.CORE,
    "c": ScoreType.CORE,
    "d": ScoreType.CORE,
}

# Override for readiness question (a/b -> starter, c/d -> core)
_READINESS_SCORING = {
    "a": ScoreType.STARTER,
    "b": ScoreType.STARTER,
    "c": ScoreType.CORE,
    "d": ScoreType.CORE,
}

SCORING_RULES = {
    "q1": _DEFAULT_SCORING,
    "q2": _DEFAULT_SCORING,
    "q3": _DEFAULT_SCORING,
    "readiness": _READINESS_SCORING,
}

# Program labels
PROGRAM_LABELS = {
    ProgramType.STARTER: "Starter",
    ProgramType.CORE: "Professional Certificate Beauty Management Strategy",
    ProgramType.CORE_REVIEW: "Professional Certificate Beauty Management Strategy (Review)",
}

# Program prices (in RM)
PROGRAM_PRICES = {
    ProgramType.STARTER: "588",
    ProgramType.CORE: "5,997",
}
