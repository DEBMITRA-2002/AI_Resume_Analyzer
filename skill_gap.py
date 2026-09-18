import pandas as pd


# =========================================================
# LEARNING ROADMAP
# =========================================================

LEARNING_ROADMAP = {

    "python": {
        "level": "Beginner to Intermediate",
        "topics": "Python basics, functions, OOP, modules, file handling",
        "project": "Build a Python-based data analysis project"
    },

    "sql": {
        "level": "Beginner to Intermediate",
        "topics": "SELECT, WHERE, JOIN, GROUP BY, subqueries, window functions",
        "project": "Build a SQL-based business data analysis project"
    },

    "excel": {
        "level": "Beginner to Intermediate",
        "topics": "Formulas, lookup functions, pivot tables, charts, dashboards",
        "project": "Create an Excel business dashboard"
    },

    "pandas": {
        "level": "Intermediate",
        "topics": "DataFrames, filtering, grouping, merging, data cleaning",
        "project": "Perform EDA on a real-world dataset"
    },

    "numpy": {
        "level": "Intermediate",
        "topics": "Arrays, indexing, broadcasting, mathematical operations",
        "project": "Implement numerical data processing with NumPy"
    },

    "power bi": {
        "level": "Beginner to Intermediate",
        "topics": "Power Query, data modeling, DAX, dashboards",
        "project": "Build an interactive Power BI dashboard"
    },

    "machine learning": {
        "level": "Intermediate",
        "topics": "Regression, classification, clustering, model evaluation",
        "project": "Build a machine learning prediction system"
    },

    "scikit-learn": {
        "level": "Intermediate",
        "topics": "Preprocessing, pipelines, classification, regression, model evaluation",
        "project": "Build an end-to-end ML project using Scikit-learn"
    },

    "deep learning": {
        "level": "Intermediate to Advanced",
        "topics": "Neural networks, CNN, backpropagation, optimization",
        "project": "Build an image classification model"
    },

    "tensorflow": {
        "level": "Intermediate",
        "topics": "Tensors, neural networks, model training, evaluation",
        "project": "Build and train a TensorFlow deep learning model"
    },

    "pytorch": {
        "level": "Intermediate",
        "topics": "Tensors, neural networks, training loops, model evaluation",
        "project": "Build a PyTorch deep learning project"
    },

    "nlp": {
        "level": "Intermediate",
        "topics": "Text preprocessing, tokenization, embeddings, text classification",
        "project": "Build an NLP text classification system"
    },

    "transformers": {
        "level": "Advanced",
        "topics": "Attention, transformer architecture, pretrained models",
        "project": "Build an NLP application using Transformers"
    },

    "hugging face": {
        "level": "Intermediate to Advanced",
        "topics": "Datasets, tokenizers, pretrained models, pipelines",
        "project": "Create an NLP application using Hugging Face"
    },

    "llm": {
        "level": "Intermediate to Advanced",
        "topics": "LLM concepts, prompting, embeddings, model APIs",
        "project": "Build an LLM-powered application"
    },

    "rag": {
        "level": "Advanced",
        "topics": "Embeddings, vector databases, retrieval, generation",
        "project": "Build a document question-answering RAG system"
    },

    "opencv": {
        "level": "Intermediate",
        "topics": "Image processing, feature detection, video processing",
        "project": "Build a computer vision application"
    },

    "cnn": {
        "level": "Intermediate",
        "topics": "Convolution, pooling, feature maps, image classification",
        "project": "Build a CNN image classifier"
    },

    "docker": {
        "level": "Intermediate",
        "topics": "Images, containers, Dockerfiles, networking",
        "project": "Containerize a machine learning application"
    },

    "fastapi": {
        "level": "Intermediate",
        "topics": "REST APIs, endpoints, request handling, API deployment",
        "project": "Create an ML model prediction API"
    },

    "git": {
        "level": "Beginner",
        "topics": "Repository, commit, branch, merge, pull request",
        "project": "Maintain a project using Git and GitHub"
    },

    "statistics": {
        "level": "Beginner to Intermediate",
        "topics": "Mean, variance, probability, distributions, hypothesis testing",
        "project": "Perform statistical analysis on a dataset"
    }
}


# =========================================================
# NORMALIZE SKILL NAME
# =========================================================

def normalize_skill(skill):
    """
    Normalize skill names for comparison.
    """

    skill = str(skill).lower().strip()

    skill = skill.replace("c #", "c#")
    skill = skill.replace("c ++", "c++")
    skill = skill.replace(". net", ".net")

    return skill


# =========================================================
# GET REQUIRED SKILLS
# =========================================================

def get_required_skills(job_role, job_file="data/job_roles.csv"):
    """
    Get required skills for a selected job role.
    """

    df = pd.read_csv(job_file)

    role_data = df[
        df["job_role"].str.lower() == job_role.lower()
    ]

    if role_data.empty:
        return []

    skills_text = role_data.iloc[0]["required_skills"]

    skills = [
        skill.strip()
        for skill in skills_text.split(",")
    ]

    return skills


# =========================================================
# FIND MISSING SKILLS
# =========================================================

def find_missing_skills(found_skills, required_skills):
    """
    Find skills required by the job role but
    missing from the resume.
    """

    resume_skills = []

    for skills in found_skills.values():

        for skill in skills:
            resume_skills.append(
                normalize_skill(skill)
            )

    resume_skills = set(resume_skills)

    missing_skills = []

    for skill in required_skills:

        normalized_required = normalize_skill(skill)

        if normalized_required not in resume_skills:
            missing_skills.append(skill)

    return missing_skills


# =========================================================
# GENERATE LEARNING ROADMAP
# =========================================================

def generate_learning_roadmap(missing_skills):
    """
    Generate a learning roadmap for missing skills.
    """

    roadmap = []

    for skill in missing_skills:

        normalized_skill = normalize_skill(skill)

        if normalized_skill in LEARNING_ROADMAP:

            roadmap_info = LEARNING_ROADMAP[
                normalized_skill
            ]

            roadmap.append({
                "Skill": skill,
                "Level": roadmap_info["level"],
                "Topics": roadmap_info["topics"],
                "Project": roadmap_info["project"]
            })

        else:

            roadmap.append({
                "Skill": skill,
                "Level": "To be determined",
                "Topics": "Learn the fundamentals and practical applications",
                "Project": f"Build a small project using {skill}"
            })

    return roadmap