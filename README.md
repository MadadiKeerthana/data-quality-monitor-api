# Data Quality Monitoring Service

## Overview
This project is a lightweight backend service that validates CSV datasets before they are used in downstream systems. It is designed to simulate an internal data quality tool that helps prevent bad data from breaking analytics pipelines, dashboards, or machine learning workflows.

The service exposes an API where users can upload a CSV file and receive a structured validation report containing errors, warnings, and summary metrics.

## Table of Contents
- [Problem](#problem)
- [Solution](#solution)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Sample Data](#sample-data)
- [Sample Output](#sample-output)
- [How It Works](#how-it-works)
- [Design Decisions](#design-decisions)
- [Future Improvements](#future-improvements)
- [Use Cases](#use-cases)
- [Author](#author)

---

## Problem
In many data-driven systems, teams rely on CSV or batch data uploads from various sources. These datasets often contain issues such as:
- Missing required fields
- Duplicate identifiers
- Invalid formats (emails, dates, numeric values)
- Inconsistent categorical values

If not caught early, these issues can:
- Break ETL pipelines
- Corrupt analytics
- Cause incorrect business decisions

---

## Solution
This service validates incoming CSV files and generates a structured report before the data is processed further.

It performs:
- Schema validation (required columns)
- Row-level validation (data correctness)
- Duplicate detection
- Summary metrics for quick analysis

---

## Features
- CSV file upload via API
- Required column validation
- Row-level data validation:
  - Missing values
  - Duplicate IDs
  - Invalid email formats
  - Invalid or missing dates
  - Negative or invalid numeric values
  - Invalid categorical values (status)
- Structured JSON response with:
  - Detailed error list
  - Summary metrics
- Interactive API testing via Swagger UI

---

## Tech Stack
- Python
- FastAPI
- Pandas
- Pydantic
- Uvicorn

---

## Project Structure


data-quality-monitor/
├── app/
│   ├── main.py
│   ├── validator.py
│   ├── rules.py
│   └── models.py
├── sample_data/
│   ├── valid_orders.csv
│   └── invalid_orders.csv
├── reports/
│   └── sample_validation_report.json
├── requirements.txt
└── README.md



---

## Installation

### 1. Clone the repository

bash
git clone <your-repo-url>
cd data-quality-monitor


### 2. Create virtual environment

bash
python -m venv venv
source venv/bin/activate


### 3. Install dependencies

bash
pip install -r requirements.txt



---

## Running the Application

Start the FastAPI server:

bash
uvicorn app.main:app --reload


Open Swagger UI:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


---

## API Endpoints

### GET /health
Returns service status.

**Response:**

json
{
  "status": "ok"
}


### POST /validate
Upload a CSV file for validation.

#### Request
- **Content-Type:** multipart/form-data
- **File:** CSV file

#### Response
Returns a structured validation report.

**Example:**

json
{
  "file_name": "invalid_orders.csv",
  "total_rows": 9,
  "total_columns": 5,
  "status": "failed",
  "errors": [
    {
      "row": 2,
      "column": "customer_email",
      "message": "Invalid email format"
    }
  ],
  "warnings": [],
  "summary": {
    "missing_values": 2,
    "duplicate_ids": 2,
    "invalid_dates": 1,
    "invalid_emails": 1,
    "negative_amounts": 1,
    "invalid_amounts": 1,
    "invalid_statuses": 1
  }
}



---

## Sample Data

### sample_data/valid_orders.csv
A clean dataset with no validation issues.

**Expected result: reports/valid_report.json**


### sample_data/invalid_orders.csv
A dataset intentionally containing:
- Invalid email format
- Duplicate order IDs
- Missing values
- Invalid dates
- Invalid amounts
- Invalid status values

**Expected result: reports/sample_validation_report.json**

---

## How It Works

1. The API receives a CSV file upload
2. The file is parsed into a pandas DataFrame
3. Validation rules are applied:
   - File-level checks (required columns)
   - Row-level checks (data correctness)
4. Errors are collected and categorized
5. Summary metrics are generated
6. A structured JSON report is returned

---

## Design Decisions

- Modular rule-based validation:
  Each validation rule is implemented as an independent function for clarity and extensibility.

- Separation of concerns:
  - rules.py handles validation logic
  - validator.py orchestrates execution
  - models.py defines response schema
  - main.py exposes API endpoints

- Typed responses using Pydantic:
  Ensures consistent and well-defined API output.

---

## Future Improvements

- Add warning-level validations (e.g., outliers)
- Support for additional file formats (JSON, Parquet)
- Config-driven validation rules
- Persistent storage of validation reports
- UI dashboard for uploading and viewing reports
- Integration with data pipelines (Airflow, etc.)

---

## Use Cases

- Pre-validation for ETL pipelines
- Data quality checks for analytics teams
- Internal tooling for data ingestion workflows
- Preventing bad data from reaching production systems

---

## Author
Keerthana Madadi

