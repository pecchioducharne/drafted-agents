"""
Worker runner - starts RQ workers to process jobs
"""

import os
import redis
from rq import Worker, Queue


def main():
    """Start RQ worker"""
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_conn = redis.from_url(redis_url)
    
    worker = Worker(["agent-jobs"], connection=redis_conn)
    print(f"🚀 Worker started, listening on queue: agent-jobs")
    print(f"   Redis: {redis_url}")
    worker.work(with_scheduler=True)


if __name__ == "__main__":
    main()
