import uuid
import threading
import time
from app.validator import validate_csv

jobs = {}


def create_job():
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing", "result": None}
    return job_id


def complete_job(job_id, result):
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["result"] = result


def get_job(job_id):
    return jobs.get(job_id)


def process_file_async(job_id, file_path):
    time.sleep(15)  # simulate processing delay
    result = validate_csv(file_path)
    complete_job(job_id, result)


def start_background_job(job_id, file_path):
    thread = threading.Thread(target=process_file_async, args=(job_id, file_path))
    thread.start()
