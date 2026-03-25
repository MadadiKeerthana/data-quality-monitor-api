import re
import pandas as pd

REQUIRED_COLUMNS = ["order_id", "customer_email", "order_date", "amount", "status"]

ALLOWED_STATUS = {"completed", "pending", "cancelled"}

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def check_required_columns(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return missing


def check_missing_values(df):
    errors = []

    for col in REQUIRED_COLUMNS:
        null_rows = df[df[col].isnull()].index.tolist()

        for row in null_rows:
            errors.append({"row": row + 1, "column": col, "message": "Missing value"})

    return errors


def check_duplicate_order_ids(df):
    errors = []
    duplicates = df[df.duplicated("order_id", keep=False)]

    for idx in duplicates.index:
        errors.append(
            {"row": idx + 1, "column": "order_id", "message": "Duplicate order_id"}
        )

    return errors


def check_email_format(df):
    errors = []

    for idx, value in df["customer_email"].items():
        if not isinstance(value, str) or not re.match(EMAIL_REGEX, value):
            errors.append(
                {
                    "row": idx + 1,
                    "column": "customer_email",
                    "message": "Invalid email format",
                }
            )

    return errors


def check_order_date(df):
    errors = []

    for idx, value in df["order_date"].items():
        if pd.isna(value):
            continue
        try:
            pd.to_datetime(value)
        except Exception:
            errors.append(
                {
                    "row": idx + 1,
                    "column": "order_date",
                    "message": "Invalid date format",
                }
            )

    return errors


def check_amount(df):
    errors = []

    for idx, value in df["amount"].items():
        try:
            if float(value) < 0:
                errors.append(
                    {
                        "row": idx + 1,
                        "column": "amount",
                        "message": "Amount cannot be negative",
                    }
                )
        except Exception:
            errors.append(
                {"row": idx + 1, "column": "amount", "message": "Invalid amount"}
            )

    return errors


def check_status(df):
    errors = []

    for idx, value in df["status"].items():
        if value not in ALLOWED_STATUS:
            errors.append(
                {
                    "row": idx + 1,
                    "column": "status",
                    "message": f"Invalid status: {value}",
                }
            )

    return errors


ROW_LEVEL_RULES = [
    check_missing_values,
    check_duplicate_order_ids,
    check_email_format,
    check_order_date,
    check_amount,
    check_status,
]
