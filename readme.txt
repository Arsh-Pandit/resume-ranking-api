# Project: AI Resume Screening & Ranking System

Input:
- Resume text (PDF or plain text)
- Job description text

Output:
- Matching score (0–100)
- Ranked list of resumes

Approach (Day 1):
- Text similarity between resume and JD
- No deep learning yet

Use case:
- Recruiters / coaching institutes / startups# AI Resume Screening & Ranking API

## Overview
This project builds a machine learning system that ranks resumes
based on similarity to a job description using TF-IDF and cosine similarity.

## Features
- Resume ranking API
- FastAPI backend
- Input validation
- Health check endpoint

## Tech Stack
- Python
- Scikit-learn
- FastAPI
- Uvicorn

## How to Run

1. Install dependencies
pip install -r requirements.txt

2. Run server
uvicorn app:app --reload

3. Visit
http://127.0.0.1:8000/docs

## Future Improvements
- Sentence Transformer embeddings
- Resume PDF upload
- Cloud deployment