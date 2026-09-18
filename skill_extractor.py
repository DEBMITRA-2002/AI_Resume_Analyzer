# Skill dictionary for the Resume Analyzer

SKILL_DICTIONARY = {
    "Programming": [
        "python",
        "java",
        "c++",
        "c#",
        "javascript",
        "typescript",
        "php",
        "r"
    ],

    "Data Analysis": [
        "pandas",
        "numpy",
        "excel",
        "power bi",
        "tableau",
        "matplotlib",
        "seaborn"
    ],

    "Database": [
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "oracle",
        "sqlite"
    ],

    "Machine Learning": [
        "machine learning",
        "scikit-learn",
        "tensorflow",
        "keras",
        "pytorch",
        "deep learning"
    ],

    "NLP & AI": [
        "nlp",
        "natural language processing",
        "transformers",
        "hugging face",
        "llm",
        "rag",
        "generative ai"
    ],

    "Computer Vision": [
        "opencv",
        "cnn",
        "yolo",
        "computer vision",
        "image processing"
    ],

    "Cloud & Deployment": [
        "aws",
        "azure",
        "google cloud",
        "docker",
        "fastapi",
        "streamlit"
    ],

    "Tools & Version Control": [
        "git",
        "github",
        "jupyter",
        "vs code",
        "visual studio"
    ],

    "Web Development": [
        "html",
        "css",
        "react",
        "node.js",
        "flask",
        "django"
    ]
}


def extract_skills(text):
    """
    Extract skills from cleaned resume text.
    """

    text = text.lower()

    found_skills = {}

    for category, skills in SKILL_DICTIONARY.items():

        category_skills = []

        for skill in skills:

            if skill.lower() in text:
                category_skills.append(skill)

        if category_skills:
            found_skills[category] = category_skills

    return found_skills