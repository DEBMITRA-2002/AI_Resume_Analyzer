# 📄 AI Resume Analyzer & Job Recommendation System

## 📌 Project Overview

AI Resume Analyzer is an NLP-based web application that analyzes a candidate's resume and compares it with predefined job-role requirements.

The system extracts resume text, cleans and normalizes the content, identifies technical skills, calculates job-role matching scores, identifies skill gaps, and generates a personalized learning roadmap.

The application is developed using Python and Streamlit.

---

## 🎯 Objectives

The main objectives of this project are:

- Extract text from PDF and DOCX resumes
- Clean and normalize resume text
- Identify technical skills from resumes
- Compare resumes with different job roles
- Calculate job-role match scores
- Recommend the top matching job roles
- Identify missing skills
- Generate a basic learning roadmap
- Provide an interactive Streamlit dashboard

---

## ✨ Features

### 📄 Resume Upload

Users can upload resumes in:

- PDF
- DOCX

### 🧹 Text Cleaning

The extracted resume text is cleaned and normalized using Python and regular expressions.

### 🧠 Skill Extraction

The system identifies technical skills using a predefined skill dictionary.

Skills are grouped into categories such as:

- Programming
- Data Analysis
- Database
- Machine Learning
- NLP & AI
- Computer Vision
- Cloud & Deployment
- Tools & Version Control
- Web Development

### 💼 Job Role Matching

The system compares the resume with predefined job roles using:

- TF-IDF Vectorization
- Cosine Similarity

### 🏆 Job Recommendations

The system displays the top 3 job roles based on the calculated match scores.

### 🔍 Skill Gap Analysis

The application identifies skills required by the target role that were not detected in the resume.

### 📚 Learning Roadmap

A basic learning roadmap is generated for identified skill gaps.

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- TF-IDF
- Cosine Similarity
- PyPDF
- python-docx
- Regular Expressions

---

## 📂 Project Structure

```text
AI_Resume_Analyzer
│
├── data
│   └── job_roles.csv
│
├── venv
│
├── app.py
├── resume_parser.py
├── text_cleaner.py
├── skill_extractor.py
├── job_matcher.py
├── skill_gap.py
├── requirements.txt
├── README.md
└── .gitignore