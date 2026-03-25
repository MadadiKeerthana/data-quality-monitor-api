from pathlib import Path
import shutil

from fastapi import FastAPI, File, UploadFile, HTTPException

from app.validator import validate_csv
from app.models import ValidationReport

app = FastAPI(title="Data Quality Monitoring Service")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/validate", response_model=ValidationReport)
async def validate_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        report = validate_csv(str(file_path))
        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

    finally:
        if file_path.exists():
            file_path.unlink()
