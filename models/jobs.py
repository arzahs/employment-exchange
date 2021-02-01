import datetime
from pydantic import BaseModel


class BaseJob(BaseModel):
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool = True

class Job(BaseJob):
    id: int
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class JobIn(BaseJob):
    pass
    