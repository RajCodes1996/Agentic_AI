from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_instruction: str | None = None,
    ) -> str:
        """Generate a text response for the given prompt."""