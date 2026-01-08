"""User data model to encapsulate context.user_data access."""

from telegram.ext import ContextTypes

from src.enums import ProgramType, Language, ReadinessAnswer
from src.models.form_data import FormData
from src.models.pain_answers import PainAnswers
from src.models.upsell_answers import UpsellAnswers


class UserData:
    """Encapsulates access to context.user_data with type safety."""

    def __init__(self, context: ContextTypes.DEFAULT_TYPE):
        """Initialize with Telegram context."""
        self._context = context
        self._user_data = context.user_data

    @property
    def lang(self) -> str | None:
        """Get user's language preference."""
        return self._user_data.get("lang")

    @lang.setter
    def lang(self, value: str) -> None:
        """Set user's language preference."""
        self._user_data["lang"] = value

    def get_language_enum(self) -> Language:
        """Get language as Language enum."""
        lang_code = self.lang or "en"
        return Language.from_code(lang_code)

    @property
    def track(self) -> str | None:
        """Get user's selected track."""
        return self._user_data.get("track")

    @track.setter
    def track(self, value: str | ProgramType) -> None:
        """Set user's selected track."""
        if isinstance(value, ProgramType):
            self._user_data["track"] = value.value
        else:
            self._user_data["track"] = value

    def get_track_enum(self) -> ProgramType | None:
        """Get track as ProgramType enum."""
        track_str = self.track
        if not track_str:
            return None
        try:
            return ProgramType(track_str)
        except ValueError:
            return None

    @property
    def program(self) -> str | None:
        """Get user's selected program."""
        return self._user_data.get("program")

    @program.setter
    def program(self, value: str | ProgramType) -> None:
        """Set user's selected program."""
        if isinstance(value, ProgramType):
            self._user_data["program"] = value.value
        else:
            self._user_data["program"] = value

    def get_program_enum(self) -> ProgramType | None:
        """Get program as ProgramType enum."""
        program_str = self.program
        if not program_str:
            return None
        try:
            return ProgramType(program_str)
        except ValueError:
            return None

    @property
    def recommendation(self) -> str | None:
        """Get recommendation result."""
        return self._user_data.get("recommendation")

    @recommendation.setter
    def recommendation(self, value: str | ProgramType) -> None:
        """Set recommendation result."""
        if isinstance(value, ProgramType):
            self._user_data["recommendation"] = value.value
        else:
            self._user_data["recommendation"] = value

    def get_recommendation_enum(self) -> ProgramType | None:
        """Get recommendation as ProgramType enum."""
        rec_str = self.recommendation
        if not rec_str:
            return None
        try:
            return ProgramType(rec_str)
        except ValueError:
            return None

    @property
    def pain_answers(self) -> dict[str, str | None]:
        """Get pain point answers as dict (for backward compatibility)."""
        pain_answers_model = self.get_pain_answers_model()
        return pain_answers_model.to_dict()

    def get_pain_answers_model(self) -> PainAnswers:
        """Get pain point answers as PainAnswers model."""
        data = self._user_data.get("pain_answers", {"q1": None, "q2": None, "q3": None})
        return PainAnswers.from_dict(data)

    def set_pain_answer(self, question: str, answer: str) -> None:
        """Set pain point answer."""
        if "pain_answers" not in self._user_data:
            self._user_data["pain_answers"] = {"q1": None, "q2": None, "q3": None}
        self._user_data["pain_answers"][question] = answer

    def set_pain_answers_model(self, pain_answers: PainAnswers) -> None:
        """Set pain point answers from PainAnswers model."""
        self._user_data["pain_answers"] = pain_answers.to_dict()

    @property
    def readiness(self) -> ReadinessAnswer | None:
        """Get readiness answer as ReadinessAnswer enum."""
        readiness_value = self._user_data.get("readiness")
        if readiness_value is None:
            return None
        # Handle both enum and string storage (backward compatibility)
        if isinstance(readiness_value, ReadinessAnswer):
            return readiness_value
        try:
            return ReadinessAnswer(readiness_value)
        except (ValueError, TypeError):
            return None

    def get_readiness_str(self) -> str | None:
        """Get readiness answer as string (for backward compatibility)."""
        readiness = self.readiness
        return readiness.value if readiness else None

    @readiness.setter
    def readiness(self, value: ReadinessAnswer | str | None) -> None:
        """Set readiness answer.

        Args:
            value: ReadinessAnswer enum, string ("a", "b", "c", "d"), or None
        """
        if value is None:
            self._user_data["readiness"] = None
        elif isinstance(value, ReadinessAnswer):
            # Store as string for JSON serialization compatibility
            self._user_data["readiness"] = value.value
        elif isinstance(value, str):
            # Validate string and convert to enum, then store as string
            try:
                readiness_enum = ReadinessAnswer(value)
                self._user_data["readiness"] = readiness_enum.value
            except ValueError:
                raise ValueError(f"Invalid readiness answer: {value}")
        else:
            raise TypeError(
                f"readiness must be ReadinessAnswer, str, or None, got {type(value)}"
            )

    @property
    def upsell_answers(self) -> dict[str, str | bool | None]:
        """Get upsell answers as dict (for backward compatibility)."""
        upsell_answers_model = self.get_upsell_answers_model()
        return upsell_answers_model.to_dict()

    def get_upsell_answers_model(self) -> UpsellAnswers:
        """Get upsell answers as UpsellAnswers model."""
        data = self._user_data.get("upsell_answers", {"has_team": None, "intent": None})
        return UpsellAnswers.from_dict(data)

    def set_upsell_answer(self, key: str, value: str | bool) -> None:
        """Set upsell answer."""
        if "upsell_answers" not in self._user_data:
            self._user_data["upsell_answers"] = {"has_team": None, "intent": None}
        self._user_data["upsell_answers"][key] = value

    def set_upsell_answers_model(self, upsell_answers: UpsellAnswers) -> None:
        """Set upsell answers from UpsellAnswers model."""
        self._user_data["upsell_answers"] = upsell_answers.to_dict()

    def _get_raw_form_data(self) -> dict[str, str | None]:
        """Get raw form data dict from storage (for internal use)."""
        default = {
            "full_name": None,
            "phone": None,
            "email": None,
            "business_type": None,
        }
        return self._user_data.get("form_data", default) or default

    @property
    def form_data(self) -> dict[str, str | None]:
        """Get form data as dict."""
        return self._get_raw_form_data().copy()

    def get_form_data_model(self) -> FormData | None:
        """Get form data as validated FormData model.

        Returns FormData only if all required fields are present and valid.
        Used for final submission, not during form entry.
        """
        data = self._get_raw_form_data()

        # Check if we have the minimum required fields
        full_name = data.get("full_name")
        phone = data.get("phone")
        business_type = data.get("business_type")

        if not full_name or not phone or not business_type:
            return None

        try:
            return FormData(
                full_name=full_name,
                phone=phone,
                email=data.get("email"),
                business_type=business_type,
            )
        except Exception as e:
            # Log validation error for debugging
            print(f"FormData validation error: {e}")
            return None

    def set_form_data(self, data: dict[str, str | None] | FormData) -> None:
        """Set form data from dict or FormData model."""
        if isinstance(data, FormData):
            self._user_data["form_data"] = {
                "full_name": data.full_name,
                "phone": data.phone,
                "email": data.email,
                "business_type": data.business_type,
            }
        else:
            self._user_data["form_data"] = data

    def update_form_field(self, field_name: str, value: str) -> None:
        """Update a single form field directly in storage."""
        # Read directly from raw storage (like set_pain_answer does)
        if "form_data" not in self._user_data:
            self._user_data["form_data"] = {
                "full_name": None,
                "phone": None,
                "email": None,
                "business_type": None,
            }
        self._user_data["form_data"][field_name] = value

    @property
    def starter_score(self) -> int:
        """Get starter score."""
        return self._user_data.get("starter_score", 0)

    @starter_score.setter
    def starter_score(self, value: int) -> None:
        """Set starter score."""
        self._user_data["starter_score"] = value

    def increment_starter_score(self) -> None:
        """Increment starter score."""
        current = self._user_data.get("starter_score", 0)
        self._user_data["starter_score"] = current + 1

    @property
    def core_score(self) -> int:
        """Get core score."""
        return self._user_data.get("core_score", 0)

    @core_score.setter
    def core_score(self, value: int) -> None:
        """Set core score."""
        self._user_data["core_score"] = value

    def increment_core_score(self) -> None:
        """Increment core score."""
        current = self._user_data.get("core_score", 0)
        self._user_data["core_score"] = current + 1

    def reset(self) -> None:
        """Reset all user data to initial state."""
        self._user_data["lang"] = None
        self._user_data["track"] = None
        self._user_data["program"] = None
        self._user_data["recommendation"] = None
        self._user_data["pain_answers"] = {"q1": None, "q2": None, "q3": None}
        self._user_data["readiness"] = None
        self._user_data["upsell_answers"] = {"has_team": None, "intent": None}
        self._user_data["form_data"] = {
            "full_name": None,
            "phone": None,
            "email": None,
            "business_type": None,
        }
        self._user_data["starter_score"] = 0
        self._user_data["core_score"] = 0
