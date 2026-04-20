from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SieveOutcome(str, Enum):
    PASS = "PASS"
    ANOMALY = "ANOMALY"
    FAILED = "FAILED"
    WARNING = "WARNING"
    ERROR = "ERROR"


class SieveStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"


class SieveResult(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    status: SieveStatus
    message: str = Field(min_length=1)


class FinalJudgement(str, Enum):
    FRAUD_DETECTED = "FRAUD_DETECTED"
    SUSPICIOUS = "SUSPICIOUS"
    VALIDATED = "VALIDATED"


class ForensicLogEntry(BaseModel):
    sieve: str
    result: SieveOutcome
    details: str
    correlation_id: str | None = None
    duration_ms: int | None = None


class AnalyzeResponse(BaseModel):
    status: Literal["Completed"] = "Completed"
    final_judgement: FinalJudgement
    forensic_log: list[ForensicLogEntry] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    code: str
    message: str
    request_id: str
    details: str | None = None


class VisionAnalysis(BaseModel):
    tampering_detected: bool = False
    risk_level: str = "LOW"
    summary: str = ""
    findings: list[str] = Field(default_factory=list)
