# Data Quality Monitoring Service with Async Job Processing

## Overview
This project is a lightweight backend service that validates CSV datasets before they are used in downstream systems. It simulates an internal data quality tool that helps prevent bad data from breaking analytics pipelines, dashboards, or machine learning workflows.

The service exposes an API where users can upload a CSV file, receive a job ID, and poll for validation results asynchronously. This design mirrors real-world batch processing systems where work is submitted first and completed later.

## Table of Contents
- [Problem](#problem)
- [Solution](#solution)
- [Why This Project Matters](#why-this-project-matters)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Sample Output](#sample-output)
- [How It Works](#how-it-works)
- [Design Decisions](#design-decisions)
- [Future Improvements](#future-improvements)
- [Use Cases](#use-cases)
- [Why This Project Matters](#why-this-project-matters)
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
This service validates incoming CSV files and generates a structured report before the data is consumed by downstream systems such as analytics pipelines, dashboards, or machine learning workflows.

It performs:
- Schema validation (required columns)
- Row-level validation (data correctness)
- Duplicate detection
- Summary metrics for quick analysis

---

## Why This Project Matters

This project demonstrates how backend systems handle data validation as an asynchronous workflow rather than a blocking request. Instead of returning results immediately, the service follows a job-based pattern where work is submitted, processed in the background, and retrieved later using a job ID.

This pattern is commonly used in:
- ETL pipelines
- Batch processing systems
- Machine learning workflows
- Internal data platforms

By implementing asynchronous job processing and status tracking, this project reflects real-world backend system design rather than a simple CRUD API.

---

## Features
- CSV file upload via API
- Asynchronous job submission
- Job status tracking using job IDs
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
- Python threading (background job processing)

---

## Project Structure

```text
data-quality-monitor/
├── app/
│   ├── main.py
│   ├── validator.py
│   ├── rules.py
│   ├── models.py
│   └── job_manager.py
├── sample_data/
│   ├── valid_orders.csv
│   └── invalid_orders.csv
├── reports/
│   ├── sample_validation_report.json
│   └── async_sample_report.json
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd data-quality-monitor
```


### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```


---

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


---

## API Endpoints

### GET /health
Returns service status.

**Response:**

```json
{
  "status": "ok"
}
```


---

### POST /jobs
Uploads a CSV file and creates an asynchronous validation job.

- Request:
  - Content-Type: multipart/form-data
  - Body: CSV file

- Behavior:
  - Saves the uploaded file
  - Creates a unique job ID
  - Starts background validation
  - Returns immediately with job status

Example response:
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "processing"
}
```

---

### GET /jobs/{job_id}
Retrieves the current status of a validation job and its result when available.

- Path Parameter:
  - job_id: string

- Behavior:
  - Returns job status
  - Returns validation result once processing is complete

Example response (processing):
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "processing",
  "result": null
}
```

Example response (completed):
```json
{
  "job_id": "c5a97f95-2617-4c27-ad88-b7d33dcdfc8f",
  "status": "completed",
  "result": {
    "file_name": "invalid_orders.csv",
    "total_rows": 9,
    "total_columns": 5,
    "status": "failed",
    "errors": [
      {
        "row": 5,
        "column": "customer_email",
        "message": "Missing value"
      },
      {
        "row": 6,
        "column": "order_date",
        "message": "Missing value"
      },
      {
        "row": 1,
        "column": "order_id",
        "message": "Duplicate order_id"
      },
      {
        "row": 4,
        "column": "order_id",
        "message": "Duplicate order_id"
      },
      {
        "row": 2,
        "column": "customer_email",
        "message": "Invalid email format"
      },
      {
        "row": 5,
        "column": "customer_email",
        "message": "Invalid email format"
      },
      {
        "row": 7,
        "column": "order_date",
        "message": "Invalid date format"
      },
      {
        "row": 3,
        "column": "amount",
        "message": "Amount cannot be negative"
      },
      {
        "row": 8,
        "column": "amount",
        "message": "Invalid amount"
      },
      {
        "row": 9,
        "column": "status",
        "message": "Invalid status: done"
      }
    ],
    "warnings": [],
    "summary": {
      "missing_values": 2,
      "duplicate_ids": 2,
      "invalid_dates": 1,
      "invalid_emails": 2,
      "negative_amounts": 1,
      "invalid_amounts": 1,
      "invalid_statuses": 1
    }
  }
}
```
---

## Sample Output

Example validation output is available in:

```text
reports/sample_validation_report.json
reports/async_sample_report.json
```
---

## How It Works

1. The API receives a CSV file upload
2. A validation job is created and assigned a unique job ID
3. The file is processed in the background
4. Validation rules are applied:
   - File-level checks (required columns)
   - Row-level checks (data correctness)
5. Errors are collected and categorized
6. Summary metrics are generated
7. The client polls the job status endpoint to retrieve the final result

---

## Design Decisions

- Modular rule-based validation:
  Each validation rule is implemented as an independent function for clarity and extensibility.

- Separation of concerns:
  - `rules.py` handles validation logic
  - `validator.py` orchestrates execution
  - `models.py` defines response schemas
  - `job_manager.py` manages async job lifecycle
  - `main.py` exposes API endpoints

- Asynchronous processing:
  Validation runs in a background thread so the API can return a job ID immediately instead of blocking until processing completes.

- Typed responses using Pydantic:
  Ensures consistent and well-defined API output.

---

## Future Improvements

- Persist jobs in a database instead of in-memory storage
- Add failed job state and error tracking
- Support downloadable validation reports
- Add warning-level validations for suspicious but non-blocking values
- Support additional file formats such as JSON and Parquet
- Replace background threads with a proper task queue such as Celery or Redis
- Build a simple frontend dashboard for job submission and status tracking

---

## Use Cases

- Pre-validation for ETL pipelines
- Data quality checks for analytics teams
- Internal tooling for data ingestion workflows
- Preventing bad data from reaching production systems

---

## Author
Keerthana Madadi

