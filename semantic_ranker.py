from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def rank_resumes(job_description, resumes):

    jd_embedding = model.encode([job_description])
    resume_embeddings = model.encode(resumes)

    scores = cosine_similarity(jd_embedding, resume_embeddings)[0]

    ranked = sorted(
        zip(resumes, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked