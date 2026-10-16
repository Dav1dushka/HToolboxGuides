"""Regression tests for the synthetic payment-risk demo."""

from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from main import load_synthetic_rows, risk_band, score_transaction


REQUIRED_FIELDS = [
    "transaction_id",
    "amount",
    "currency",
    "billing_country",
    "ip_country",
    "attempts_last_10m",
    "account_age_days",
    "avs_match",
    "cvc_match",
    "synthetic_data",
]


def event(**overrides: str) -> dict[str, str]:
    row = {
        "transaction_id": "SYN-TEST-1",
        "amount": "25.00",
        "currency": "EUR",
        "billing_country": "CZ",
        "ip_country": "CZ",
        "attempts_last_10m": "1",
        "account_age_days": "90",
        "avs_match": "true",
        "cvc_match": "true",
        "synthetic_data": "true",
    }
    row.update(overrides)
    return row


class RiskScoringTests(unittest.TestCase):
    def test_low_risk_event_has_no_rules_triggered(self) -> None:
        score, reasons = score_transaction(event())
        self.assertEqual(score, 0)
        self.assertEqual(reasons, [])
        self.assertEqual(risk_band(score), "LOW — no rule triggered")

    def test_multiple_signals_cap_score_at_100(self) -> None:
        score, reasons = score_transaction(
            event(
                amount="900",
                billing_country="CZ",
                ip_country="US",
                attempts_last_10m="6",
                account_age_days="0",
                avs_match="false",
                cvc_match="false",
            )
        )
        self.assertEqual(score, 100)
        self.assertGreaterEqual(len(reasons), 5)
        self.assertEqual(risk_band(score), "HIGH — manual review")

    def test_medium_band(self) -> None:
        score, reasons = score_transaction(
            event(
                amount="500",
                attempts_last_10m="3",
                account_age_days="4",
            )
        )
        self.assertEqual(score, 40)
        self.assertEqual(risk_band(score), "MEDIUM — review")
        self.assertTrue(reasons)

    def test_risk_band_boundaries(self) -> None:
        self.assertEqual(risk_band(29), "LOW — no rule triggered")
        self.assertEqual(risk_band(30), "MEDIUM — review")
        self.assertEqual(risk_band(59), "MEDIUM — review")
        self.assertEqual(risk_band(60), "HIGH — manual review")


class InputGuardTests(unittest.TestCase):
    def write_csv(self, rows: list[dict[str, str]], fields: list[str]) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "input.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def test_rejects_sensitive_card_columns(self) -> None:
        fields = REQUIRED_FIELDS + ["pan"]
        path = self.write_csv([event(pan="4242424242424242")], fields)
        with self.assertRaisesRegex(ValueError, "Sensitive card fields"):
            load_synthetic_rows(path)

    def test_rejects_non_synthetic_rows(self) -> None:
        path = self.write_csv([event(synthetic_data="false")], REQUIRED_FIELDS)
        with self.assertRaisesRegex(ValueError, "not marked synthetic_data=true"):
            load_synthetic_rows(path)

    def test_accepts_synthetic_rows(self) -> None:
        path = self.write_csv([event()], REQUIRED_FIELDS)
        rows = load_synthetic_rows(path)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["transaction_id"], "SYN-TEST-1")


if __name__ == "__main__":
    unittest.main()
