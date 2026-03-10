from pydantic import BaseModel
from typing import List

class RankedResume(BaseModel):
    resume_id: int
    score: float
    skills_found : List[str]

class RankResponse(BaseModel):
    ranked_resumes: List[RankedResume]