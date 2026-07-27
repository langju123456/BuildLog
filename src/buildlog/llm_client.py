"""LiteLLM client wrapper for BuildLog model calls."""

from __future__ import annotations

import json
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from buildlog.config import Settings
from buildlog.exceptions import ModelResponseError, StructuredOutputError

SchemaT = TypeVar("SchemaT", bound=BaseModel)


class LLMClient:
    """Small LiteLLM wrapper for text and structured JSON responses."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def complete_text(self, prompt: str) -> str:
        """Return a plain text model completion."""
        response = self._completion(prompt)
        content = _extract_content(response)
        if not content.strip():
            raise ModelResponseError("model returned empty content")
        return content.strip()

    def complete_json(self, prompt: str, schema: type[SchemaT]) -> SchemaT:
        """Return a Pydantic-validated JSON model completion."""
        raw = self.complete_text(prompt)
        try:
            data = json.loads(_strip_json_fence(raw))
        except json.JSONDecodeError as exc:
            raise StructuredOutputError(f"model returned invalid JSON: {exc.msg}") from exc

        try:
            return schema.model_validate(data)
        except ValidationError as exc:
            raise StructuredOutputError(str(exc)) from exc

    def _completion(self, prompt: str) -> object:
        try:
            from litellm import completion

            kwargs: dict[str, object] = {
                "model": self._settings.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": self._settings.temperature,
                "max_tokens": self._settings.max_tokens,
            }
            if self._settings.api_base:
                kwargs["api_base"] = self._settings.api_base
            return completion(**kwargs)
        except Exception as exc:
            raise ModelResponseError(f"model call failed: {exc}") from exc


def _extract_content(response: object) -> str:
    try:
        choices = getattr(response, "choices")
        message = choices[0].message
        content = message.content
    except (AttributeError, IndexError, TypeError) as exc:
        raise ModelResponseError("model response did not contain message content") from exc
    return str(content)


def _strip_json_fence(raw: str) -> str:
    text = raw.strip()
    if text.startswith("```json"):
        text = text.removeprefix("```json").strip()
    elif text.startswith("```"):
        text = text.removeprefix("```").strip()
    if text.endswith("```"):
        text = text.removesuffix("```").strip()
    return text
