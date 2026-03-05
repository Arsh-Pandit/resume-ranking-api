import os
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def load_documents(path):
    files=[]
    file_names=[]
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            file_names.append(filename)
            with open(os.path.join(path, filename), "r", encoding="utf-8") as f:
                files.append(f.read())
    return files, file_names

def build_vectorizer(corpus):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1,2),
        max_df=0.9,
        min_df=1
        )
    
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return vectorizer, tfidf_matrix

def rank_resumes(resumes, jd, vectorizer):

    # Combine job description and resumes
    documents = [jd] + resumes

    # Convert text to TF-IDF vectors
    vectors = vectorizer.transform(documents)

    # First vector = job description
    jd_vector = vectors[0]

    # Remaining vectors = resumes
    resume_vectors = vectors[1:]

    # Compute similarity between JD and each resume
    similarity_scores = cosine_similarity(resume_vectors, jd_vector)

    # Convert to list of (resume_index, score)
    results = [(i, similarity_scores[i][0]) for i in range(len(resumes))]

    # Sort resumes by score
    results.sort(key=lambda x: x[1], reverse=True)

    return results