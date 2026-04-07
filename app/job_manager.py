import uuid
import threading
import time
import json
import traceback
from app.validator import validate_csv
from app.database import SessionLocal
from app.db_models import Job

def create_job():
    db = SessionLocal()
    job_id = str(uuid.uuid4())
    job = Job(
        id= job_id,
        status= "processing",
        result= None
    )
    
    db.add(job)
    db.commit()
    db.close()
    
    return job_id


def complete_job(job_id, result):
    db = SessionLocal()
    
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job.status = "completed"
        job.result = json.dumps(result.model_dump())
        db.commit()
    
    db.close()


def get_job(job_id):
    db = SessionLocal()
    
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        db.close()
        return None


    result = {
        "status": job.status,
        "result": json.loads(job.result) if job.result else None
    }
    
    db.close()
    return result


def process_file_async(job_id, file_path):
    try:
        # time.sleep(15)  # simulate processing delay
        result = validate_csv(file_path)
        complete_job(job_id, result)
    except Exception as e:
        print(f"Job {job_id} failed with error: {e}")
        traceback.print_exc()
        
        db = SessionLocal()
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = "failed"
            db.commit()
        db.close()


def start_background_job(job_id, file_path):
    thread = threading.Thread(target=process_file_async, args=(job_id, file_path))
    thread.start()
