from fastapi import FastAPI
from fastapi import UploadFile, File, Form
from pdf_parser import extract_text_from_pdf
from skill_extractor import extract_skills


from schemas.rank_schemas import RankRequest, RankResponse
from semantic_ranker import rank_resumes
from fastapi import HTTPException

app = FastAPI()




@app.post("/rank", response_model=RankResponse)
def rank_endpoint(request: RankRequest):

    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    if not request.resumes:
        raise HTTPException(status_code=400, detail="Resume list cannot be empty")

    results = rank_resumes(
        jd = request.job_description,
        resumes = request.resumes
    )

    response = []
    for i, (resume_text, score) in enumerate(results):
        skills = extract_skills(resume_text)
        response.append({
            "resume_id": i + 1,
            "score": round(score * 100, 2),
            "skills_found": skills
        })

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
        jd=job_description,
        resumes=resume_texts
    )

    response = []
    for i, (resume_text, score) in enumerate(ranked):

        skills = extract_skills(resume_text)

        response.append({
            "resume_id": i + 1,
            "score": round(score * 100, 2),
            "skills_found": skills
        })

    return {"ranked_resumes": response}

@app.get("/health")
def health_check():
    return {"status": "ok"}