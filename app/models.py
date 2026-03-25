from typing import List, Optional
from pydantic import BaseModel


class ValidationIssue(BaseModel):
    row: Optional[int]
    column: str
    message: str


class ValidationSummary(BaseModel):
    missing_values: int
    duplicate_ids: int
    invalid_dates: int
    invalid_emails: int
    negative_amounts: int
    invalid_amounts: int
    invalid_statuses: int


class ValidationReport(BaseModel):
    file_name: str
    total_rows: int
    total_columns: int
    status: str
    errors: List[ValidationIssue]
    warnings: List[ValidationIssue]
    summary: ValidationSummary
