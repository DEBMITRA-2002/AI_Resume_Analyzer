import re


def clean_resume_text(text):
    """
    Clean and normalize extracted resume text.
    """

    # Convert text to lowercase
    text = text.lower()

    # Normalize common technical skills
    text = text.replace("c ++", "c++")
    text = text.replace("c #", "c#")
    text = text.replace(". net", ".net")

    # Remove unnecessary characters
    text = re.sub(r"[^\w\s+#.]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove leading and trailing spaces
    text = text.strip()

    return text