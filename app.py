from fastapi import FastAPI
import joblib
from fastapi import UploadFile, File, Form
from pdf_parser import extract_text_from_pdf


from schemas.rank_schemas import RankRequest, RankResponse
from semantic_ranker import rank_resumes
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

@app.post("/rank-pdf", response_model=RankResponse)
async def rank_pdf(
    job_description: str = Form(...),
    resumes: UploadFile = File(...)
):

    resume_texts = []

    for file in resumes:
        contents = await file.read()
        text = extract_text_from_pdf(contents)
        resume_texts.append(text)

    ranked = rank_resumes(
        resumes=resume_texts,
        jd=job_description,
        vectorizer=vectorizer
    )

    response = [
        {"resume_id": idx + 1, "score": round(score * 100, 2)}
        for idx, score in ranked
    ]

    return {"ranked_resumes": response}

@app.get("/health")
def health_check():
    return {"status": "ok"}