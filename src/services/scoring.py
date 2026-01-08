"""Scoring service for diagnosis questions."""

from src.constants import SCORING_RULES
from src.enums import ProgramType, ScoreType


class ScoreCalculator:
    """Handles scoring logic for diagnosis questions."""

    def __init__(self, user_data):
        """Initialize with user data accessor."""
        self.user_data = user_data

    def update_score(self, question: str, answer: str) -> None:
        """Update score based on question answer.

        Args:
            question: Question key (q1, q2, q3, readiness)
            answer: Answer key (a, b, c, d)
        """
        score_type = SCORING_RULES.get(question, {}).get(answer, ScoreType.STARTER)

        if score_type == ScoreType.STARTER:
            self.user_data.increment_starter_score()
        else:
            self.user_data.increment_core_score()

    def calculate_recommendation(self) -> ProgramType:
        """Calculate recommendation based on scores.

        Returns:
            ProgramType.CORE if core_score > starter_score, otherwise ProgramType.STARTER
            (tie favors Starter)
        """
        if self.user_data.core_score > self.user_data.starter_score:
            return ProgramType.CORE
        return ProgramType.STARTER


class RecommendationCalculator:
    """Calculates program recommendations."""

    @staticmethod
    def determine_recommendation(starter_score: int, core_score: int) -> ProgramType:
        """Determine recommendation based on scores.

        Args:
            starter_score: Starter program score
            core_score: Core program score

        Returns:
            ProgramType.CORE if core_score > starter_score, otherwise ProgramType.STARTER
        """
        if core_score > starter_score:
            return ProgramType.CORE
        return ProgramType.STARTER
