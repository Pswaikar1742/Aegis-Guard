from __future__ import annotations

from sieves.benford import _mad_against_benford, analyze_benford


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


def test_mad_against_benford_is_low_for_benford_like_values() -> None:
    mad, usable = _mad_against_benford(_benford_like_values())
    assert usable > 900
    assert mad < 0.015


def test_analyze_benford_passes_for_benford_like_distribution(monkeypatch) -> None:
    values = _benford_like_values()
    monkeypatch.setattr("sieves.benford._extract_numbers_via_llm", lambda _text: values)

    entry, extracted = analyze_benford("")

    assert len(extracted) >= 900
    assert entry.sieve == "Statistical"
    assert entry.result.value == "PASS"
    assert "MAD=" in entry.details


def test_analyze_benford_flags_anomaly_for_uniform_distribution(monkeypatch) -> None:
    values = _uniform_values()
    monkeypatch.setattr("sieves.benford._extract_numbers_via_llm", lambda _text: values)

    entry, extracted = analyze_benford("")

    assert len(extracted) >= 1000
    assert entry.result.value == "ANOMALY"
    assert "non-conforming" in entry.details


def test_analyze_benford_warns_for_small_sample(monkeypatch) -> None:
    monkeypatch.setattr("sieves.benford._extract_numbers_via_llm", lambda _text: [101.0, 202.0, 303.0])

    entry, extracted = analyze_benford("")

    assert extracted == [101.0, 202.0, 303.0]
    assert entry.result.value == "WARNING"
    assert "needs at least" in entry.details
