from pydantic import BaseModel
from typing import List

class RankRequest(BaseModel):
    job_description: str
    resumes: list[str]

class RankedResume(BaseModel):
    resume_id: int
    score: float
    skills_found : List[str]

class RankResponse(BaseModel):
    ranked_resumes: list[RankedResume]