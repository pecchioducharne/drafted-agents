"""
Orchestrator API - LangGraph Brain for Drafted Agents
"""
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import yaml
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Drafted Orchestrator API", version="0.1.0")


class TaskRequest(BaseModel):
    """Task request model"""
    request: str
    context: Optional[Dict[str, Any]] = None
    repo: Optional[str] = None
    ticket: Optional[str] = None
    constraints: Optional[List[str]] = None
    risk_level: Optional[str] = "medium"


class TaskResponse(BaseModel):
    """Task response model"""
    task_id: str
    status: str
    message: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "drafted-orchestrator",
        "status": "ok",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "temporal": "connected",  # TODO: actual check
            "mcp_servers": "connected",  # TODO: actual check
            "vector_store": "connected"  # TODO: actual check
        }
    }


@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskRequest):
    """
    Create a new task for the agent system
    
    This will:
    1. Parse and validate the request
    2. Route to appropriate persona + skills
    3. Start a Temporal workflow
    4. Return task ID for tracking
    """
    # TODO: Implement full orchestration logic
    # For now, return a placeholder response
    
    task_id = f"task_{hash(task.request) % 10000}"
    
    return TaskResponse(
        task_id=task_id,
        status="queued",
        message=f"Task created and queued for processing"
    )


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get status of a task"""
    # TODO: Query Temporal workflow status
    return {
        "task_id": task_id,
        "status": "running",
        "progress": "Analyzing request..."
    }


@app.get("/personas")
async def list_personas():
    """List available personas"""
    personas_dir = "/app/workflows/personas"
    personas = []
    
    try:
        for filename in os.listdir(personas_dir):
            if filename.endswith('.yml'):
                with open(os.path.join(personas_dir, filename), 'r') as f:
                    persona = yaml.safe_load(f)
                    personas.append(persona)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"personas": personas}


@app.get("/skills")
async def list_skills():
    """List available skills"""
    skills_dir = "/app/workflows/skills"
    skills = []
    
    try:
        for filename in os.listdir(skills_dir):
            if filename.endswith('.yml'):
                with open(os.path.join(skills_dir, filename), 'r') as f:
                    skill = yaml.safe_load(f)
                    skills.append(skill)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"skills": skills}


@app.get("/workflows")
async def list_workflows():
    """List available workflow templates"""
    workflows_dir = "/app/workflows/templates"
    workflows = []
    
    try:
        for filename in os.listdir(workflows_dir):
            if filename.endswith('.yml'):
                with open(os.path.join(workflows_dir, filename), 'r') as f:
                    workflow = yaml.safe_load(f)
                    workflows.append(workflow)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"workflows": workflows}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
