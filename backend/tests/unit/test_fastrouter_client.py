from __future__ import annotations

from types import SimpleNamespace

import pytest

from core.fastrouter_client import call_json_with_fallback


class _FakeCompletions:
    def __init__(self, scripted_results):
        self._scripted_results = iter(scripted_results)

    def create(self, **_kwargs):
        result = next(self._scripted_results)
        if isinstance(result, Exception):
            raise result
        return result


class _FakeClient:
    def __init__(self, scripted_results):
        self.chat = SimpleNamespace(completions=_FakeCompletions(scripted_results))


def _completion_with_json(payload: str):
    message = SimpleNamespace(content=payload)
    choice = SimpleNamespace(message=message)
    return SimpleNamespace(choices=[choice])


def test_call_json_with_fallback_retries_and_then_succeeds(monkeypatch) -> None:
    scripted_results = [
        RuntimeError("attempt-1 json-mode failure"),
        RuntimeError("attempt-1 fallback failure"),
        _completion_with_json('{"gstins": ["27ABCDE1234F1Z0"]}'),
    ]

    monkeypatch.setattr("core.fastrouter_client._get_client", lambda: _FakeClient(scripted_results))

    payload, used_model = call_json_with_fallback(
        models=["model-A"],
        messages=[{"role": "user", "content": "extract"}],
        max_retries_per_model=1,
        retry_backoff_sec=0,
    )

    assert used_model == "model-A"
    assert payload == {"gstins": ["27ABCDE1234F1Z0"]}


def test_call_json_with_fallback_raises_after_all_models_fail(monkeypatch) -> None:
    scripted_results = [
        RuntimeError("m1 attempt 1 json failure"),
        RuntimeError("m1 attempt 1 fallback failure"),
        RuntimeError("m2 attempt 1 json failure"),
        RuntimeError("m2 attempt 1 fallback failure"),
    ]
    monkeypatch.setattr("core.fastrouter_client._get_client", lambda: _FakeClient(scripted_results))

    with pytest.raises(RuntimeError) as exc_info:
        call_json_with_fallback(
            models=["model-A", "model-B"],
            messages=[{"role": "user", "content": "extract"}],
            max_retries_per_model=0,
            retry_backoff_sec=0,
        )

    message = str(exc_info.value)
    assert "All FastRouter model calls failed" in message
    assert "model-A" in message
    assert "model-B" in message
