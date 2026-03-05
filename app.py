from fastapi import FastAPI
import joblib

from schemas.rank_schemas import RankRequest, RankResponse
from ranking import rank_resumes
from fastapi import HTTPException

app = FastAPI()

# Load model artifacts once (important)
vectorizer = joblib.load("models/tfidf_vectorizer.joblib")



@app.post("/rank", response_model=RankResponse)
def rank_endpoint(request: RankRequest):

    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    if not request.resumes:
        raise HTTPException(status_code=400, detail="Resume list cannot be empty")

    results = rank_resumes(
        resumes=request.resumes,
        jd=request.job_description,
        vectorizer=vectorizer
    )

    response = [
        {"resume_id": idx+1, "score": round(score * 100, 2)}
        for idx, score in results
    ]

    return {"ranked_resumes": response}

@app.get("/health")
def health_check():
    return {"status": "ok"}