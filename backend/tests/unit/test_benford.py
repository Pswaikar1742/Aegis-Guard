from __future__ import annotations

from sieves.benford import analyze_benford, calculate_variance_score


def _benford_like_values() -> list[float]:
    # Counts approximate the Benford expected distribution across first digits 1..9.
    counts = {
        1: 301,
        2: 176,
        3: 125,
        4: 97,
        5: 79,
        6: 67,
        7: 58,
        8: 51,
        9: 46,
    }
    values: list[float] = []
    for digit, count in counts.items():
        for idx in range(count):
            values.append(float(f"{digit}{idx + 100}"))
    return values


def _uniform_values() -> list[float]:
    values: list[float] = []
    for digit in range(1, 10):
        for idx in range(120):
            values.append(float(f"{digit}{idx + 500}"))
    return values


def _to_invoice_text(values: list[float]) -> str:
    return " ".join(str(item) for item in values)


def test_mad_against_benford_is_low_for_benford_like_values() -> None:
    variance = calculate_variance_score(_benford_like_values())
    assert variance < 0.0002


def test_analyze_benford_passes_for_benford_like_distribution() -> None:
    values = _benford_like_values()

    entry, extracted = analyze_benford(_to_invoice_text(values))

    assert len(extracted) >= 900
    assert entry.sieve == "Statistical"
    assert entry.result.value == "PASS"
    assert "variance score=" in entry.details


def test_analyze_benford_flags_anomaly_for_uniform_distribution() -> None:
    values = _uniform_values()

    entry, extracted = analyze_benford(_to_invoice_text(values))

    assert len(extracted) >= 1000
    assert entry.result.value == "FAILED"
    assert "non-conforming" in entry.details


def test_analyze_benford_warns_for_small_sample() -> None:
    entry, extracted = analyze_benford("101 202 303")

    assert extracted == [101.0, 202.0, 303.0]
    assert entry.result.value == "WARNING"
    assert "needs at least" in entry.details
