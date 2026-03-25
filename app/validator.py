from pathlib import Path
import pandas as pd

from app.rules import check_required_columns, ROW_LEVEL_RULES
from app.models import ValidationIssue, ValidationSummary, ValidationReport


def build_summary(errors):
    summary = {
        "missing_values": 0,
        "duplicate_ids": 0,
        "invalid_dates": 0,
        "invalid_emails": 0,
        "negative_amounts": 0,
        "invalid_amounts": 0,
        "invalid_statuses": 0,
    }

    for error in errors:
        message = error["message"]

        if message == "Missing value":
            summary["missing_values"] += 1
        elif message == "Duplicate order_id":
            summary["duplicate_ids"] += 1
        elif message == "Invalid date format":
            summary["invalid_dates"] += 1
        elif message == "Invalid email format":
            summary["invalid_emails"] += 1
        elif message == "Amount cannot be negative":
            summary["negative_amounts"] += 1
        elif message == "Invalid amount":
            summary["invalid_amounts"] += 1
        elif message.startswith("Invalid status"):
            summary["invalid_statuses"] += 1

    return ValidationSummary(**summary)


def validate_csv(file_path):
    df = pd.read_csv(file_path)

    total_rows = len(df)
    total_columns = len(df.columns)
    file_name = Path(file_path).name

    missing_columns = check_required_columns(df)
    if missing_columns:
        errors = [
            ValidationIssue(row=None, column=col, message="Missing required column")
            for col in missing_columns
        ]

        return ValidationReport(
            file_name=file_name,
            total_rows=total_rows,
            total_columns=total_columns,
            status="failed",
            errors=errors,
            warnings=[],
            summary=ValidationSummary(
                missing_values=0,
                duplicate_ids=0,
                invalid_dates=0,
                invalid_emails=0,
                negative_amounts=0,
                invalid_amounts=0,
                invalid_statuses=0,
            ),
        )

    raw_errors = []

    for rule in ROW_LEVEL_RULES:
        raw_errors.extend(rule(df))

    errors = [ValidationIssue(**error) for error in raw_errors]
    summary = build_summary(raw_errors)

    return ValidationReport(
        file_name=file_name,
        total_rows=total_rows,
        total_columns=total_columns,
        status="passed" if not errors else "failed",
        errors=errors,
        warnings=[],
        summary=summary,
    )
