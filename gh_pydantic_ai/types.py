from typing import Any, Literal

type Headers = dict[str, str]
type DataStrAny = dict[str, Any]

type GHCopilotModelName = Literal[
    # claude models
    "claude-haiku-4.5",
    "claude-opus-4.5",
    "claude-opus-4.6",
    "claude-opus-4.7",
    "claude-opus-4.8",
    "claude-opus-5",
    "claude-sonnet-4.5",
    "claude-sonnet-4.6",
    "claude-sonnet-5",
    # gemini models
    "gemini-2.5-pro",
    "gemini-3-flash-preview",
    "gemini-3.1-pro-preview",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    # openai models
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0613",
    "gpt-4",
    "gpt-4-0125-preview",
    "gpt-4-0613",
    "gpt-4-o-preview",
    "gpt-4.1",
    "gpt-4.1-2025-04-14",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-2024-08-06",
    "gpt-4o-2024-11-20",
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
    "gpt-5-mini",
    "gpt-5.3-codex",
    "gpt-5.4",
    "gpt-5.4-mini",
    "gpt-5.5",
    "gpt-5.6-luna",
    "gpt-5.6-sol",
    "gpt-5.6-terra",
    # grok
    "grok-4.5",
    # other models
    "mai-code-1-flash-picker",
    "text-embedding-3-small",
    "text-embedding-3-small-inference",
    "text-embedding-ada-002",
    "trajectory-compaction",
]

__all__ = [
    "DataStrAny",
    "GHCopilotModelName",
    "Headers",
]
