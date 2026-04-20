from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class SieveOutcome(str, Enum):
    PASS = "PASS"
    ANOMALY = "ANOMALY"
    FAILED = "FAILED"
    WARNING = "WARNING"
    ERROR = "ERROR"


class FinalJudgement(str, Enum):
    FRAUD_DETECTED = "FRAUD_DETECTED"
    SUSPICIOUS = "SUSPICIOUS"
    VALIDATED = "VALIDATED"


class ForensicLogEntry(BaseModel):
    sieve: str
    result: SieveOutcome
    details: str


class AnalyzeResponse(BaseModel):
    status: Literal["Completed"] = "Completed"
    final_judgement: FinalJudgement
    forensic_log: list[ForensicLogEntry] = Field(default_factory=list)


class VisionAnalysis(BaseModel):
    tampering_detected: bool = False
    risk_level: str = "LOW"
    summary: str = ""
    findings: list[str] = Field(default_factory=list)
