import json
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_list_setting(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        raw_value = value.strip()
        if not raw_value:
            return []
        if raw_value.startswith("["):
            try:
                parsed = json.loads(raw_value)
            except json.JSONDecodeError:
                parsed = None
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        return [item.strip() for item in raw_value.split(",") if item.strip()]
    raise TypeError("Expected list or comma-separated string.")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        enable_decoding=False,
        extra="ignore",
    )

    app_name: str = "Aegis Guard Backend"
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])

    # Fail-fast: this key is required for boot.
    fastrouter_api_key: str = Field(..., min_length=20)
    fastrouter_base_url: str = "https://api.fastrouter.ai/v1"

    extraction_models: list[str] = Field(
        default_factory=lambda: [
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o-mini",
        ]
    )
    vision_models: list[str] = Field(
        default_factory=lambda: [
            "openai/gpt-4o",
            "google/gemini-1.5-pro",
        ]
    )

    suspicious_pdf_creators: list[str] = Field(
        default_factory=lambda: [
            "canva",
            "photoshop",
            "illustrator",
            "figma",
            "coreldraw",
        ]
    )

    benford_min_sample_size: int = 40

    @field_validator(
        "cors_origins",
        "extraction_models",
        "vision_models",
        "suspicious_pdf_creators",
        mode="before",
    )
    @classmethod
    def validate_list_settings(cls, value: Any) -> list[str]:
        return _parse_list_setting(value)

    @field_validator("fastrouter_api_key", mode="before")
    @classmethod
    def validate_fastrouter_api_key(cls, value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("FASTROUTER_API_KEY is required.")
        return value.strip()


settings = Settings()
