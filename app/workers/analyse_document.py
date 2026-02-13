# # 
# Find a pending job

# SELECT *
# FROM analysis_jobs
# WHERE status = 'PENDING'
# ORDER BY created_at ASC
# LIMIT 1;
# # 


# Set the pending job to running:

# UPDATE analysis_jobs
# SET status = 'RUNNING',
#     started_at = now()
# WHERE id = :job_id;


# mark it as completed

# UPDATE analysis_jobs
# SET status = 'COMPLETED',
#     completed_at = now(),
#     result = :json_result
# WHERE id = :job_id;

import time
from datetime import datetime
from sqlalchemy import select


from app.db.session import SessionLocal
from app.db.models import AnalysisJob, AnalysisStatus


def run():
    while True:
        with SessionLocal() as db:
            statement = (
                select(AnalysisJob)
                .where(AnalysisJob.status == AnalysisStatus.PENDING)
                .order_by(AnalysisJob.created_at.asc())
                .limit(1)
            )

            job = db.execute(statement).scalar_one_or_none()

            if job:
                job.status = AnalysisStatus.RUNNING
                job.started_at = datetime.utcnow()
                db.commit()

                # simulate analysis
                result = {
                    "summary": "This is a mock summary."
                }

                job.result = result
                job.status = AnalysisStatus.COMPLETED
                job.completed_at = datetime.utcnow()
                db.commit()

        time.sleep(1)

if __name__ == "__main__":
    run()
    