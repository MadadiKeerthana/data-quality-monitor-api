from pathlib import Path
import shutil

from fastapi import FastAPI, File, UploadFile, HTTPException

from app.validator import validate_csv
from app.models import ValidationReport
from app.job_manager import create_job, start_background_job, get_job

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
            

@app.post("/jobs")
async def create_validation_job(file: UploadFile = File(...)):
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    file_path = upload_dir / file.filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
        job_id = create_job()
        
        start_background_job(job_id, str(file_path))
        
        return {
            "job_id": job_id,
            "status": "processing"
        }


@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    job = get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job_id,
        "status": job["status"],
        "result": job["result"]
    }
    
    
