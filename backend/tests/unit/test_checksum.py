from __future__ import annotations

from sieves.checksum import analyze_checksum, validate_gstin


def _gstin_with_valid_check_digit(payload_14_chars: str) -> str:
    for digit in "0123456789":
        candidate = payload_14_chars + digit
        if validate_gstin(candidate):
            return candidate
    raise AssertionError("Unable to generate GSTIN with valid checksum digit for test payload.")


def test_gstin_checksum_accepts_valid_value() -> None:
    valid_gstin = _gstin_with_valid_check_digit("27ABCDE1234F1Z")
    assert validate_gstin(valid_gstin) is True


def test_gstin_checksum_rejects_invalid_check_char() -> None:
    valid_gstin = _gstin_with_valid_check_digit("29PQRSX6789L1Z")
    replacement = "0" if valid_gstin[-1] != "0" else "1"
    invalid_gstin = valid_gstin[:-1] + replacement
    assert validate_gstin(invalid_gstin) is False


def test_gstin_checksum_rejects_invalid_length() -> None:
    assert validate_gstin("27ABCDE1234F1Z") is False


def test_analyze_checksum_classifies_failed_when_any_gstin_invalid() -> None:
    valid_gstin = _gstin_with_valid_check_digit("07LMNOP4321Q1Z")
    invalid_gstin = valid_gstin[:-1] + ("0" if valid_gstin[-1] != "0" else "1")

    entry, gstins = analyze_checksum(f"primary={valid_gstin} secondary={invalid_gstin}")

    assert set(gstins) == {valid_gstin, invalid_gstin}
    assert entry.sieve == "Checksum"
    assert entry.result.value == "FAILED"
    assert invalid_gstin in entry.details
