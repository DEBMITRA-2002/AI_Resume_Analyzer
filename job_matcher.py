import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Path of the job-role dataset
JOB_ROLE_FILE = "data/job_roles.csv"


def load_job_roles():
    """
    Load job roles and required skills from CSV file.
    """

    df = pd.read_csv(JOB_ROLE_FILE)

    return df


def calculate_match_score(resume_text, required_skills):
    """
    Calculate similarity between resume text
    and required job skills using TF-IDF
    and cosine similarity.
    """

    documents = [
        resume_text,
        required_skills
    ]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    score = round(similarity * 100, 2)

    return score


def match_resume_to_jobs(resume_text):
    """
    Compare resume with all available job roles
    and return match scores.
    """

    job_roles = load_job_roles()

    results = []

    for _, row in job_roles.iterrows():

        job_role = row["job_role"]
        required_skills = row["required_skills"]

        score = calculate_match_score(
            resume_text,
            required_skills
        )

        results.append({
            "Job Role": job_role,
            "Match Score": score
        })

    results_df = pd.DataFrame(results)

    # Sort from highest score to lowest score
    results_df = results_df.sort_values(
        by="Match Score",
        ascending=False
    ).reset_index(drop=True)

    return results_df