#!/usr/bin/env python3
"""
CLI for Drafted Agent Brain

Usage:
    brain run "Fix issue #123" --repo drafted-web --issue 123
    brain status <job_id>
    brain logs <job_id>
"""

import os
import sys
import click
import httpx
import time


API_URL = os.getenv("BRAIN_API_URL", "http://localhost:7000")


@click.group()
def cli():
    """Drafted Agent Brain CLI"""
    pass


@cli.command()
@click.argument("request")
@click.option("--repo", default=None, help="Repository name")
@click.option("--issue", type=int, default=None, help="Issue number")
@click.option("--pr", type=int, default=None, help="PR number")
@click.option("--job-type", default="issue_to_pr", help="Job type")
def run(request, repo, issue, pr, job_type):
    """Submit a new job to the agent system"""
    
    click.echo(f"🚀 Submitting job...")
    click.echo(f"   Request: {request}")
    if repo:
        click.echo(f"   Repo: {repo}")
    if issue:
        click.echo(f"   Issue: #{issue}")
    
    payload = {
        "request": request,
        "job_type": job_type,
    }
    
    if repo:
        payload["repo"] = repo
    if issue:
        payload["issue"] = issue
    if pr:
        payload["pr"] = pr
    
    try:
        response = httpx.post(f"{API_URL}/jobs", json=payload, timeout=30.0)
        response.raise_for_status()
        
        data = response.json()
        job_id = data["job_id"]
        
        click.echo(f"\n✓ Job submitted: {job_id}")
        click.echo(f"   Status: {data['status']}")
        click.echo(f"\nTrack progress:")
        click.echo(f"   brain status {job_id}")
        click.echo(f"   brain logs {job_id} --follow")
        
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("job_id")
def status(job_id):
    """Get status of a job"""
    
    try:
        response = httpx.get(f"{API_URL}/jobs/{job_id}")
        response.raise_for_status()
        
        data = response.json()
        
        click.echo(f"Job ID: {job_id}")
        click.echo(f"Status: {data['status']}")
        
        if data.get("created_at"):
            click.echo(f"Created: {data['created_at']}")
        
        if data.get("result"):
            click.echo(f"\nResult:")
            result = data["result"]
            if result.get("persona"):
                click.echo(f"  Persona: {result['persona']}")
            if result.get("outputs"):
                click.echo(f"  Outputs: {result['outputs']}")
            if result.get("artifacts"):
                click.echo(f"  Artifacts:")
                for key, value in result["artifacts"].items():
                    click.echo(f"    - {key}: {value}")
        
        if data.get("error"):
            click.echo(f"\nError: {data['error']}", err=True)
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            click.echo(f"✗ Job {job_id} not found", err=True)
        else:
            click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("job_id")
@click.option("--follow", "-f", is_flag=True, help="Follow logs in real-time")
def logs(job_id, follow):
    """Get logs for a job"""
    
    try:
        if follow:
            click.echo(f"Following logs for {job_id} (Ctrl+C to stop)...")
            last_status = None
            
            while True:
                response = httpx.get(f"{API_URL}/jobs/{job_id}")
                response.raise_for_status()
                data = response.json()
                
                if data["status"] != last_status:
                    click.echo(f"\nStatus: {data['status']}")
                    last_status = data["status"]
                
                if data.get("result") and data["result"].get("logs"):
                    for log in data["result"]["logs"]:
                        click.echo(log)
                
                if data["status"] in ["completed", "failed", "cancelled"]:
                    break
                
                time.sleep(2)
        else:
            response = httpx.get(f"{API_URL}/jobs/{job_id}")
            response.raise_for_status()
            data = response.json()
            
            if data.get("result") and data["result"].get("logs"):
                for log in data["result"]["logs"]:
                    click.echo(log)
            else:
                click.echo("No logs available yet")
                
    except KeyboardInterrupt:
        click.echo("\n\nStopped following logs")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def health():
    """Check API health"""
    
    try:
        response = httpx.get(f"{API_URL}/health")
        response.raise_for_status()
        
        data = response.json()
        
        click.echo(f"Status: {data['status']}")
        click.echo(f"Redis: {data['redis']}")
        click.echo(f"Queue size: {data.get('queue_size', 'unknown')}")
        
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
