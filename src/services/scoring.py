"""Scoring service for diagnosis questions."""

from src.constants import SCORING_RULES
from src.enums import ProgramType, ScoreType
from src.services.logging_config import get_logger

logger = get_logger(__name__)


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

        logger.debug(
            "Score updated",
            extra={
                "event": "score_updated",
                "question": question,
                "answer": answer,
                "score_type": score_type.value,
                "starter_score": self.user_data.starter_score,
                "core_score": self.user_data.core_score,
            },
        )

    def calculate_recommendation(self) -> ProgramType:
        """Calculate recommendation based on scores.

        Returns:
            ProgramType.CORE if core_score > starter_score, otherwise ProgramType.STARTER
            (tie favors Starter)
        """
        if self.user_data.core_score > self.user_data.starter_score:
            recommendation = ProgramType.CORE
        else:
            recommendation = ProgramType.STARTER

        logger.debug(
            "Recommendation calculated",
            extra={
                "event": "recommendation_calculated",
                "starter_score": self.user_data.starter_score,
                "core_score": self.user_data.core_score,
                "recommendation": recommendation.value,
            },
        )

        return recommendation

    def recalculate_scores(self) -> None:
        """Recalculate scores from all stored answers.

        This method resets scores to 0 and then re-applies scoring rules
        for all present answers (q1, q2, q3, readiness). Useful when
        answers are changed via back navigation or editing.
        """
        # Reset scores
        self.user_data.starter_score = 0
        self.user_data.core_score = 0

        # Get all stored answers
        pain_answers = self.user_data.pain_answers
        readiness = self.user_data.readiness

        # Re-apply scoring for each answer
        for question in ["q1", "q2", "q3"]:
            answer = pain_answers.get(question)
            if answer:
                self.update_score(question, answer)

        # Re-apply scoring for readiness
        if readiness:
            self.update_score("readiness", readiness.value)

        logger.debug(
            "Scores recalculated",
            extra={
                "event": "score_recalculated",
                "starter_score": self.user_data.starter_score,
                "core_score": self.user_data.core_score,
            },
        )


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
