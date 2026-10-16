#!/usr/bin/env python3
"""Local synthetic payment-risk scoring demo.

This script is intentionally limited to synthetic transaction events. It does
not handle card numbers, BINs, CVVs, card dumps, or external services.
Python 3.9+; standard library only.
"""

from __future__ import annotations

import argparse
import csv
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

REQUIRED_COLUMNS = {
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
}
FORBIDDEN_COLUMNS = {
    "pan",
    "primary_account_number",
    "card_number",
    "credit_card_number",
    "cvv",
    "cvc",
    "track_data",
    "track1",
    "track2",
    "bin",
    "iin",
}


def parse_bool(value: str, field: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise ValueError(f"{field} must be true/false, yes/no, or 1/0")


def score_transaction(row: dict[str, str]) -> tuple[int, list[str]]:
    """Return an illustrative 0–100 score and readable reasons."""
    score = 0
    reasons: list[str] = []

    amount = Decimal(row["amount"])
    attempts = int(row["attempts_last_10m"])
    account_age = int(row["account_age_days"])
    avs_match = parse_bool(row["avs_match"], "avs_match")
    cvc_match = parse_bool(row["cvc_match"], "cvc_match")

    if amount >= Decimal("500"):
        score += 15
        reasons.append("high amount for this demo")
    if row["billing_country"].strip().upper() != row["ip_country"].strip().upper():
        score += 20
        reasons.append("billing country differs from IP country")
    if attempts >= 5:
        score += 30
        reasons.append("many attempts in 10 minutes")
    elif attempts >= 3:
        score += 15
        reasons.append("several attempts in 10 minutes")
    if account_age <= 1:
        score += 20
        reasons.append("very new account")
    elif account_age <= 7:
        score += 10
        reasons.append("recently created account")
    if not avs_match:
        score += 15
        reasons.append("address verification mismatch")
    if not cvc_match:
        score += 20
        reasons.append("security-code verification failed")

    return min(score, 100), reasons


def risk_band(score: int) -> str:
    if score >= 60:
        return "HIGH — manual review"
    if score >= 30:
        return "MEDIUM — review"
    return "LOW — no rule triggered"


def load_synthetic_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as file_handle:
        reader = csv.DictReader(file_handle)
        headers = {header.strip().lower() for header in (reader.fieldnames or [])}

        forbidden = headers & FORBIDDEN_COLUMNS
        if forbidden:
            raise ValueError(
                "Sensitive card fields are not accepted by this demo: "
                + ", ".join(sorted(forbidden))
            )
        missing = REQUIRED_COLUMNS - headers
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))

        rows = []
        for line_number, raw_row in enumerate(reader, start=2):
            # Normalize header and values without retaining unrecognized data.
            row = {str(k).strip().lower(): (v or "").strip()
                   for k, v in raw_row.items() if k is not None}
            if not parse_bool(row.get("synthetic_data", ""), "synthetic_data"):
                raise ValueError(
                    f"Line {line_number} is not marked synthetic_data=true; "
                    "real transaction data is not supported."
                )
            if not row.get("transaction_id"):
                raise ValueError(f"Line {line_number}: transaction_id is required.")
            # Validate before scoring so malformed data does not silently pass.
            try:
                if Decimal(row["amount"]) < 0:
                    raise ValueError("amount cannot be negative")
                if int(row["attempts_last_10m"]) < 0 or int(row["account_age_days"]) < 0:
                    raise ValueError("attempts and account age cannot be negative")
            except (InvalidOperation, KeyError) as exc:
                raise ValueError(f"Line {line_number}: invalid numeric value.") from exc
            rows.append(row)
        return rows


def run(input_path: Path, output_path: Path) -> int:
    rows = load_synthetic_rows(input_path)
    output_fields = ["transaction_id", "risk_score", "risk_band", "reasons"]

    with output_path.open("w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=output_fields)
        writer.writeheader()
        for row in rows:
            score, reasons = score_transaction(row)
            writer.writerow({
                "transaction_id": row["transaction_id"],
                "risk_score": score,
                "risk_band": risk_band(score),
                "reasons": "; ".join(reasons) if reasons else "no demo rule triggered",
            })

    print(f"Reviewed {len(rows)} synthetic events.")
    print(f"Report written to: {output_path}")
    print("Reminder: this illustrative score is not a real payment decision.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Score synthetic payment events for fraud-prevention education."
    )
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("sample_transactions.csv"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("risk_report.csv"))
    args = parser.parse_args()

    try:
        return run(args.input, args.output)
    except (OSError, ValueError, InvalidOperation, csv.Error) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
