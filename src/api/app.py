"""
FastAPI application - Job submission and status API
"""

import os
import uuid
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
from rq import Queue

from src.interfaces import TaskContext


# Initialize FastAPI
app = FastAPI(
    title="Drafted Agent Brain API",
    description="Submit tasks to the agent system",
    version="0.1.0"
)

# Initialize Redis connection
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_conn = redis.from_url(redis_url)
job_queue = Queue("agent-jobs", connection=redis_conn)


# Request/Response models
class JobRequest(BaseModel):
    """Job submission request"""
    request: str
    repo: Optional[str] = None
    issue: Optional[int] = None
    pr: Optional[int] = None
    constraints: list[str] = []
    job_type: str = "issue_to_pr"


class JobResponse(BaseModel):
    """Job submission response"""
    job_id: str
    status: str
    message: str


class JobStatus(BaseModel):
    """Job status response"""
    job_id: str
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None
    created_at: Optional[str] = None
    started_at: Optional[str] = None
    ended_at: Optional[str] = None


@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "drafted-agent-brain",
        "status": "ok",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    try:
        redis_conn.ping()
        redis_status = "connected"
    except Exception:
        redis_status = "disconnected"
    
    return {
        "status": "healthy" if redis_status == "connected" else "degraded",
        "redis": redis_status,
        "queue_size": job_queue.count if redis_status == "connected" else "unknown"
    }


@app.post("/jobs", response_model=JobResponse)
async def create_job(job_request: JobRequest):
    """
    Submit a new job to the agent system.
    
    The job will be processed asynchronously by a worker.
    """
    # Create task context
    task_id = str(uuid.uuid4())
    context = TaskContext(
        task_id=task_id,
        job_type=job_request.job_type,
        request=job_request.request,
        repo=job_request.repo or os.getenv("GITHUB_DEFAULT_REPO"),
        issue=str(job_request.issue) if job_request.issue else None,
        pr=str(job_request.pr) if job_request.pr else None,
        constraints=job_request.constraints,
        created_at=datetime.utcnow().isoformat()
    )
    
    # Enqueue job
    from src.worker.processor import process_job
    
    job = job_queue.enqueue(
        process_job,
        context.__dict__,
        job_id=task_id,
        job_timeout='30m'
    )
    
    return JobResponse(
        job_id=task_id,
        status="queued",
        message=f"Job {task_id} queued for processing"
    )


@app.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """
    Get status of a job.
    """
    from rq.job import Job
    
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        
        status_map = {
            "queued": "queued",
            "started": "running",
            "finished": "completed",
            "failed": "failed",
            "canceled": "cancelled"
        }
        
        return JobStatus(
            job_id=job_id,
            status=status_map.get(job.get_status(), "unknown"),
            result=job.result if job.is_finished else None,
            error=str(job.exc_info) if job.is_failed else None,
            created_at=job.created_at.isoformat() if job.created_at else None,
            started_at=job.started_at.isoformat() if job.started_at else None,
            ended_at=job.ended_at.isoformat() if job.ended_at else None
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found: {str(e)}")


@app.get("/jobs")
async def list_jobs(limit: int = 10):
    """List recent jobs"""
    from rq.registry import FinishedJobRegistry, StartedJobRegistry, FailedJobRegistry
    
    # Get jobs from different registries
    finished = FinishedJobRegistry(queue=job_queue)
    started = StartedJobRegistry(queue=job_queue)
    failed = FailedJobRegistry(queue=job_queue)
    
    jobs = []
    
    # Add finished jobs
    for job_id in finished.get_job_ids()[:limit]:
        from rq.job import Job
        try:
            job = Job.fetch(job_id, connection=redis_conn)
            jobs.append({
                "job_id": job_id,
                "status": "completed",
                "created_at": job.created_at.isoformat() if job.created_at else None
            })
        except Exception:
            pass
    
    return {"jobs": jobs[:limit]}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7000))
    uvicorn.run(app, host="0.0.0.0", port=port)
