import joblib
from ranking import load_documents,build_vectorizer,rank_resumes


resumes_path = r"D:\Resume_Screening\data\resumes"
job_desc_path = r"D:\Resume_Screening\data\job_description"


resumes, resume_files = load_documents(resumes_path)
job_desc, job_files = load_documents(job_desc_path)


all_documents = resumes + job_desc

vectorizer, tfidf_matrix = build_vectorizer(all_documents)

model_path = r"D:\Resume_Screening\models\tfidf_vectorizer.joblib"
joblib.dump(vectorizer, model_path)

for i, jd in enumerate(job_desc):

    print(f"\nRanking for Job Description: {job_files[i]}\n")

    results = rank_resumes(resumes, jd, vectorizer)

    for idx, score in results:
        print(f"{resume_files[idx]} → {score*100:.2f}")

