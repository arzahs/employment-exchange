from typing import List
from models.jobs import Job, JobIn
from models.user import User
from repositories.jobs import JobRepository
from fastapi import APIRouter, Depends, HTTPException, status
from .depends import get_job_repository, get_current_user

router = APIRouter()

@router.get("/", response_model=List[Job])
async def read_jobs(
    limit: int = 100,
    skip: int = 0,
    jobs: JobRepository = Depends(get_job_repository)):
    return await jobs.get_all(limit=limit, skip=skip)

@router.post("/", response_model=Job)
async def create_job(
    j: JobIn, 
    jobs: JobRepository = Depends(get_job_repository),
    current_user: User = Depends(get_current_user)):
    return await jobs.create(user_id=current_user.id, j=j)

@router.put("/", response_model=Job)
async def update_job(
    id: int,
    j: JobIn, 
    jobs: JobRepository = Depends(get_job_repository),
    current_user: User = Depends(get_current_user)):
    job = await jobs.get_by_id(id=id)
    if job is None or job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return await jobs.update(id=id, user_id=current_user.id, j=j)

@router.delete("/")
async def delete_job(id: int,
    jobs: JobRepository = Depends(get_job_repository),
    current_user: User = Depends(get_current_user)):
    job = await jobs.get_by_id(id=id)
    not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job is None or job.user_id != current_user.id:
        raise not_found_exception
    result = await jobs.delete(id=id)
    return {"status": True}