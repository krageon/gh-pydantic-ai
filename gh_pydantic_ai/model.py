from warnings import deprecated

from openai import AsyncOpenAI
from openai.types import chat
from pydantic_ai import ModelResponse, ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIResponsesModel, _ChatCompletion
from pydantic_ai.profiles import ModelProfileSpec
from pydantic_ai.providers import Provider
from typing_extensions import Any

from .consts import DEFAULT_MODEL, RESPONSES_API_MODELS
from .provider import GHCopilotProvider
from .types import GHCopilotModelName


def _normalise_completion(data: dict[str, Any]) -> dict[str, Any]:
    """Anthropic replies through gh copilot aren't openai-compliant so validation will fail.

    This injects some things that might be missing
    """
    data.setdefault("object", "chat.completion")

    choices = data.get("choices") or []
    for i, choice in enumerate(choices):
        # `index` is absent on Anthropic responses.
        choice.setdefault("index", i)
        if choice.get("finish_reason") is None:
            choice["finish_reason"] = "stop"

        message = choice.get("message")
        if message is None:
            message = {}
            choice["message"] = message
        message.setdefault("role", "assistant")

    return data

class GHCopilotChatModel(OpenAIChatModel):
    def __init__(
        self,
        model_name: GHCopilotModelName | None,
        *,
        provider: Provider[AsyncOpenAI] | None = None,
        profile: ModelProfileSpec | None = None,
        settings: ModelSettings | None = None,
    ) -> None:
        super().__init__(
            model_name=model_name or DEFAULT_MODEL,
            provider=provider or GHCopilotProvider(),
            profile=profile,
            settings=settings,
        )

    def _validate_completion(self, response: chat.ChatCompletion) -> _ChatCompletion:
        data = _normalise_completion(response.model_dump())
        return _ChatCompletion.model_validate(data)

    def _process_response(self, response: chat.ChatCompletion | str) -> ModelResponse:
        if isinstance(response, chat.ChatCompletion):
            response.object = response.object or "chat.completion"

        return super()._process_response(response)


@deprecated(
    "GHCopilotModel is deprecated and will be removed in a future release. "
    "Please use GHCopilotChatModel or GHCopilotResponsesModel instead.",
)
class GHCopilotModel(GHCopilotChatModel):
    pass


class GHCopilotResponsesModel(OpenAIResponsesModel):
    def __init__(
        self,
        model_name: GHCopilotModelName,
        *,
        provider: Provider[AsyncOpenAI] | None = None,
        profile: ModelProfileSpec | None = None,
        settings: ModelSettings | None = None,
    ) -> None:
        super().__init__(
            model_name=model_name,
            provider=provider or GHCopilotProvider(),
            profile=profile,
            settings=settings,
        )


def resolve_gh_model(
    model_name: GHCopilotModelName | None,
    *,
    provider: Provider[AsyncOpenAI] | None = None,
    profile: ModelProfileSpec | None = None,
    settings: ModelSettings | None = None,
) -> GHCopilotChatModel | GHCopilotResponsesModel:
    model_name = model_name or DEFAULT_MODEL

    if model_name in RESPONSES_API_MODELS:
        return GHCopilotResponsesModel(
            model_name=model_name,
            provider=provider,
            profile=profile,
            settings=settings,
        )

    return GHCopilotChatModel(
        model_name=model_name,
        provider=provider,
        profile=profile,
        settings=settings,
    )


__all__ = [
    "GHCopilotChatModel",
    "GHCopilotModel",
    "GHCopilotResponsesModel",
    "resolve_gh_model",
]
