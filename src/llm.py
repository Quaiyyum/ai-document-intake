"""One wrapper around the LLM. Provider and model come from .env, so no vendor is hard-coded.

Supports LLM_PROVIDER=anthropic and LLM_PROVIDER=openai (any OpenAI-compatible API via LLM_BASE_URL).
Responses are cached on disk, so a rerun of the same prompt costs nothing and is repeatable.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time

import requests
from dotenv import load_dotenv

from .common import CACHE_DIR

RETRY_WAITS = (2, 4, 8)
TIMEOUT = 120


class LLMError(RuntimeError):
    pass


class BudgetExceeded(LLMError):
    pass


class ConfigError(LLMError):
    """.env is missing or incomplete. Stops the run instead of failing every document."""


def _settings() -> dict:
    load_dotenv()
    settings = {
        "provider": (os.getenv("LLM_PROVIDER") or "").strip().lower(),
        "model": (os.getenv("LLM_MODEL") or "").strip(),
        "key": (os.getenv("LLM_API_KEY") or "").strip(),
        "base_url": (os.getenv("LLM_BASE_URL") or "").strip().rstrip("/"),
        "max_calls": int(os.getenv("LLM_MAX_CALLS") or 80),
    }
    names = {"provider": "LLM_PROVIDER", "model": "LLM_MODEL", "key": "LLM_API_KEY"}
    missing = [label for name, label in names.items() if not settings[name]]
    if missing:
        raise ConfigError(f"missing in .env: {', '.join(missing)}")
    return settings


def model_name() -> str:
    load_dotenv()
    return (os.getenv("LLM_MODEL") or "unknown").strip()


def _count_file():
    return CACHE_DIR / "call_count.txt"


def calls_made() -> int:
    path = _count_file()
    return int(path.read_text()) if path.exists() else 0


def _record_call() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    _count_file().write_text(str(calls_made() + 1))


def parse_json(text: str) -> dict:
    text = text.strip()
    fenced = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.S)
    if fenced:
        text = fenced.group(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end <= start:
            raise
        return json.loads(text[start : end + 1])


def _call_anthropic(settings: dict, system: str, user: str) -> str:
    url = (settings["base_url"] or "https://api.anthropic.com") + "/v1/messages"
    body = {
        "model": settings["model"],
        "max_tokens": 2000,
        "temperature": 0,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    headers = {"x-api-key": settings["key"], "anthropic-version": "2023-06-01"}
    response = requests.post(url, json=body, headers=headers, timeout=TIMEOUT)
    if response.status_code == 400 and "temperature" in response.text:
        body.pop("temperature")
        response = requests.post(url, json=body, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    return "".join(block.get("text", "") for block in response.json()["content"])


def _call_openai(settings: dict, system: str, user: str) -> str:
    url = (settings["base_url"] or "https://api.openai.com/v1") + "/chat/completions"
    body = {
        "model": settings["model"],
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
    }
    headers = {"Authorization": f"Bearer {settings['key']}"}
    response = requests.post(url, json=body, headers=headers, timeout=TIMEOUT)
    if response.status_code == 400 and "temperature" in response.text:
        body.pop("temperature")
        response = requests.post(url, json=body, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


PROVIDERS = {"anthropic": _call_anthropic, "openai": _call_openai}


def complete_json(system: str, user: str) -> dict:
    settings = _settings()
    if settings["provider"] not in PROVIDERS:
        raise ConfigError(f"LLM_PROVIDER must be one of {sorted(PROVIDERS)}")
    key = hashlib.sha256(
        "\x1f".join([settings["provider"], settings["model"], system, user]).encode("utf-8")
    ).hexdigest()
    cache_file = CACHE_DIR / f"{key}.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))

    last_error: Exception | None = None
    for attempt in range(len(RETRY_WAITS) + 1):
        if calls_made() >= settings["max_calls"]:
            raise BudgetExceeded(f"LLM_MAX_CALLS={settings['max_calls']} reached; stop and ask")
        _record_call()
        try:
            result = parse_json(PROVIDERS[settings["provider"]](settings, system, user))
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
            return result
        except (requests.RequestException, ValueError, KeyError) as error:
            last_error = error
            if attempt < len(RETRY_WAITS):
                time.sleep(RETRY_WAITS[attempt])
    raise LLMError(f"LLM call failed after retries: {last_error}")
