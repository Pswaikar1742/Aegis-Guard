from __future__ import annotations

import re
from typing import Any

from core.fastrouter_client import call_json_with_fallback
from core.models import SieveResult, SieveStatus


GSTIN_PATTERN = re.compile(r"^\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[0-9]$")
STATE_CODE_REGION = {
    "01": "Jammu and Kashmir",
    "02": "Himachal Pradesh",
    "03": "Punjab",
    "04": "Chandigarh",
    "05": "Uttarakhand",
    "06": "Haryana",
    "07": "Delhi",
    "08": "Rajasthan",
    "09": "Uttar Pradesh",
    "10": "Bihar",
    "11": "Sikkim",
    "12": "Arunachal Pradesh",
    "13": "Nagaland",
    "14": "Manipur",
    "15": "Mizoram",
    "16": "Tripura",
    "17": "Meghalaya",
    "18": "Assam",
    "19": "West Bengal",
    "20": "Jharkhand",
    "21": "Odisha",
    "22": "Chhattisgarh",
    "23": "Madhya Pradesh",
    "24": "Gujarat",
    "25": "Daman and Diu",
    "26": "Dadra and Nagar Haveli",
    "27": "Maharashtra",
    "29": "Karnataka",
    "30": "Goa",
    "31": "Lakshadweep",
    "32": "Kerala",
    "33": "Tamil Nadu",
    "34": "Puducherry",
    "35": "Andaman and Nicobar",
    "36": "Telangana",
    "37": "Andhra Pradesh",
}


def _state_from_gstin(gstin: str) -> str:
    return STATE_CODE_REGION.get(gstin[:2], "Unknown")


def _call_registry_model(*, vendor_name: str, gstin: str, region: str) -> dict[str, Any]:
    payload, _used_model = call_json_with_fallback(
        models=["anthropic/claude-3.5-sonnet"],
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an invoice registry verification assistant. Return strict JSON only with keys "
                    "matched (boolean), confidence (number 0-1), rationale (string), and region_consistency "
                    "(boolean)."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Vendor Name: {vendor_name}\n"
                    f"GSTIN: {gstin}\n"
                    f"GST Region: {region}\n\n"
                    "Check whether the vendor identity appears consistent with the GSTIN and region. "
                    "If unsure, keep confidence low and matched=false."
                ),
            },
        ],
        max_tokens=500,
    )
    return payload


def run_registry_sieve(*, vendor_name: str, gstin: str) -> SieveResult:
    clean_vendor = (vendor_name or "").strip()
    clean_gstin = (gstin or "").strip().upper()

    if not clean_vendor or not clean_gstin:
        return SieveResult(
            status=SieveStatus.WARNING,
            message="Registry check skipped because vendor name or GSTIN is missing.",
        )

    if not GSTIN_PATTERN.fullmatch(clean_gstin):
        return SieveResult(
            status=SieveStatus.FAIL,
            message="Registry check failed because GSTIN format is invalid.",
        )

    region = _state_from_gstin(clean_gstin)

    try:
        payload = _call_registry_model(vendor_name=clean_vendor, gstin=clean_gstin, region=region)
    except Exception as exc:
        return SieveResult(
            status=SieveStatus.WARNING,
            message=f"Registry verification degraded: {exc}",
        )

    matched = bool(payload.get("matched", False))
    region_consistency = bool(payload.get("region_consistency", False))
    confidence_raw = payload.get("confidence", 0)
    try:
        confidence = float(confidence_raw)
    except (TypeError, ValueError):
        confidence = 0.0
    rationale = str(payload.get("rationale", "No rationale provided.")).strip()

    if matched and region_consistency and confidence >= 0.5:
        return SieveResult(
            status=SieveStatus.PASS,
            message=(
                f"Registry verification passed for vendor '{clean_vendor}' and GSTIN '{clean_gstin}' "
                f"(region={region}, confidence={confidence:.2f}). {rationale}"
            ),
        )

    return SieveResult(
        status=SieveStatus.FAIL,
        message=(
            f"Registry verification failed for vendor '{clean_vendor}' and GSTIN '{clean_gstin}' "
            f"(region={region}, confidence={confidence:.2f}). {rationale}"
        ),
    )
