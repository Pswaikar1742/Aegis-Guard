from __future__ import annotations

from sieves.checksum import GSTIN_CHARSET, analyze_checksum, gstin_checksum


def _gstin_with_valid_check_char(payload_14_chars: str) -> str:
    factor = 2
    total = 0
    charset_index = {char: index for index, char in enumerate(GSTIN_CHARSET)}

    for char in reversed(payload_14_chars):
        codepoint = charset_index[char]
        addend = factor * codepoint
        factor = 1 if factor == 2 else 2
        addend = (addend // 36) + (addend % 36)
        total += addend

    checksum_value = (36 - (total % 36)) % 36
    return payload_14_chars + GSTIN_CHARSET[checksum_value]


def test_gstin_checksum_accepts_valid_value() -> None:
    valid_gstin = _gstin_with_valid_check_char("27ABCDE1234F1Z")
    assert gstin_checksum(valid_gstin) is True


def test_gstin_checksum_rejects_invalid_check_char() -> None:
    valid_gstin = _gstin_with_valid_check_char("29PQRSX6789L1Z")
    replacement = "A" if valid_gstin[-1] != "A" else "B"
    invalid_gstin = valid_gstin[:-1] + replacement
    assert gstin_checksum(invalid_gstin) is False


def test_gstin_checksum_rejects_invalid_length() -> None:
    assert gstin_checksum("27ABCDE1234F1Z") is False


def test_analyze_checksum_classifies_failed_when_any_gstin_invalid(monkeypatch) -> None:
    valid_gstin = _gstin_with_valid_check_char("07LMNOP4321Q1Z")
    invalid_gstin = valid_gstin[:-1] + ("0" if valid_gstin[-1] != "0" else "1")

    monkeypatch.setattr(
        "sieves.checksum._extract_gstin_candidates_via_llm",
        lambda _text: [valid_gstin, invalid_gstin],
    )

    entry, gstins = analyze_checksum("no regex gstin present")

    assert set(gstins) == {valid_gstin, invalid_gstin}
    assert entry.sieve == "Checksum"
    assert entry.result.value == "FAILED"
    assert invalid_gstin in entry.details
