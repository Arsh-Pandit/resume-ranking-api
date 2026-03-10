from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List, Annotated
from pydantic import WithJsonSchema

from pdf_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from semantic_ranker import rank_resumes
from schemas.rank_schemas import RankResponse

app = FastAPI()

SwaggerFile = Annotated[
    UploadFile, 
    WithJsonSchema({"type": "string", "format": "binary"})
]

@app.post("/rank-pdf", response_model=RankResponse)
async def rank_pdf(
    job_description: Annotated[str, Form()],
    resumes: List[SwaggerFile] = File(...)
):

    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    if not resumes:
        raise HTTPException(status_code=400, detail="At least one resume must be uploaded")

    resume_texts = []

    for file in resumes:

        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

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