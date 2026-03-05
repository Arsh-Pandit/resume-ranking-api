from pydantic import BaseModel

class RankRequest(BaseModel):
    job_description: str
    resumes: list[str]

class RankedResume(BaseModel):
    resume_id: int
    score: float

class RankResponse(BaseModel):
    ranked_resumes: list[RankedResume]