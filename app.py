import streamlit as st
import pandas as pd

from resume_parser import extract_resume_text
from text_cleaner import clean_resume_text
from skill_extractor import extract_skills
from job_matcher import match_resume_to_jobs
from skill_gap import (
    get_required_skills,
    find_missing_skills,
    generate_learning_roadmap
)

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 27px;
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    .info-box {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'NLP-based Resume Analysis & Job Recommendation System'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Upload your resume to analyze your skills, "
    "job-role compatibility, skill gaps, and personalized learning roadmap."
)

st.divider()

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ Project Information")

    st.write(
        """
        **AI Resume Analyzer** uses Natural Language Processing
        and Machine Learning techniques to analyze resumes.
        """
    )

    st.markdown("### 🔧 Technologies")

    st.write(
        """
        - Python
        - Streamlit
        - Pandas
        - Scikit-learn
        - TF-IDF
        - Cosine Similarity
        - PyPDF
        - python-docx
        """
    )

    st.markdown("### 📌 Features")

    st.write(
        """
        ✅ Resume Upload  
        ✅ Text Extraction  
        ✅ Text Cleaning  
        ✅ Skill Detection  
        ✅ Job Matching  
        ✅ Top 3 Job Roles  
        ✅ Skill Gap Analysis  
        ✅ Learning Roadmap
        """
    )

# ---------------------------------------------------------
# RESUME UPLOAD
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📤 Upload Your Resume</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose your resume file",
    type=["pdf", "docx"],
    help="Upload a PDF or DOCX resume."
)

# ---------------------------------------------------------
# MAIN ANALYSIS
# ---------------------------------------------------------

if uploaded_file is not None:

    st.success(
        f"Resume uploaded successfully: {uploaded_file.name} ✅"
    )

    try:

        # -------------------------------------------------
        # STEP 1: EXTRACT TEXT
        # -------------------------------------------------

        resume_text = extract_resume_text(uploaded_file)

        # -------------------------------------------------
        # STEP 2: CLEAN TEXT
        # -------------------------------------------------

        cleaned_text = clean_resume_text(resume_text)

        # -------------------------------------------------
        # STEP 3: EXTRACT SKILLS
        # -------------------------------------------------

        found_skills = extract_skills(cleaned_text)

        total_skills = sum(
            len(skills)
            for skills in found_skills.values()
        )

        # -------------------------------------------------
        # STEP 4: JOB MATCHING
        # -------------------------------------------------

        job_results = match_resume_to_jobs(cleaned_text)

        # -------------------------------------------------
        # TARGET ROLE
        # -------------------------------------------------

        if not job_results.empty:

            target_role = job_results.iloc[0]["Job Role"]

            required_skills = get_required_skills(
                target_role
            )

            missing_skills = find_missing_skills(
                found_skills,
                required_skills
            )

            learning_roadmap = generate_learning_roadmap(
                missing_skills
            )

        else:

            target_role = None
            required_skills = []
            missing_skills = []
            learning_roadmap = []

        # =================================================
        # DASHBOARD SUMMARY
        # =================================================

        st.markdown(
            '<div class="section-title">📊 Resume Analysis Summary</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Skills Detected",
                total_skills
            )

        with col2:

            if not job_results.empty:
                highest_score = job_results.iloc[0]["Match Score"]

                st.metric(
                    "Highest Match",
                    f"{highest_score:.2f}%"
                )

            else:
                st.metric(
                    "Highest Match",
                    "N/A"
                )

        with col3:

            st.metric(
                "Job Roles",
                len(job_results)
            )

        with col4:

            st.metric(
                "Skill Gaps",
                len(missing_skills)
            )

        # =================================================
        # RESUME TEXT
        # =================================================

        st.markdown(
            '<div class="section-title">📄 Extracted Resume Text</div>',
            unsafe_allow_html=True
        )

        if cleaned_text.strip():

            with st.expander(
                "View cleaned resume text"
            ):

                st.text_area(
                    "Resume Content",
                    cleaned_text,
                    height=300
                )

            st.success(
                "Resume text extracted and cleaned successfully! ✅"
            )

        else:

            st.warning(
                "No text could be extracted from this resume."
            )

        # =================================================
        # SKILLS DETECTED
        # =================================================

        st.markdown(
            '<div class="section-title">🧠 Skills Detected</div>',
            unsafe_allow_html=True
        )

        if found_skills:

            for category, skills in found_skills.items():

                st.markdown(
                    f"### 🔹 {category}"
                )

                skill_text = ", ".join(
                    skill.title()
                    for skill in skills
                )

                st.write(skill_text)

        else:

            st.info(
                "No matching skills were detected "
                "from the current skill dictionary."
            )

        # =================================================
        # JOB ROLE MATCHING
        # =================================================

        st.markdown(
            '<div class="section-title">💼 Job Role Matching</div>',
            unsafe_allow_html=True
        )

        st.write(
            "The resume is compared with available job roles "
            "using TF-IDF and cosine similarity."
        )

        if not job_results.empty:

            display_results = job_results.copy()

            display_results["Match Score"] = (
                display_results["Match Score"].map(
                    lambda x: f"{x:.2f}%"
                )
            )

            st.dataframe(
                display_results,
                use_container_width=True,
                hide_index=True
            )

        # =================================================
        # TOP 3 ROLES
        # =================================================

        st.markdown(
            '<div class="section-title">🏆 Top 3 Job Roles</div>',
            unsafe_allow_html=True
        )

        if not job_results.empty:

            top_3 = job_results.head(3).copy()

            top_3 = top_3.reset_index(
                drop=True
            )

            top_3.insert(
                0,
                "Rank",
                range(
                    1,
                    len(top_3) + 1
                )
            )

            st.dataframe(
                top_3,
                use_container_width=True,
                hide_index=True
            )

            # Role cards

            columns = st.columns(
                len(top_3)
            )

            medals = [
                "🥇",
                "🥈",
                "🥉"
            ]

            for index, column in enumerate(columns):

                with column:

                    role = top_3.iloc[index]["Job Role"]

                    score = top_3.iloc[index]["Match Score"]

                    st.metric(
                        f"{medals[index]} Role",
                        role,
                        f"{score:.2f}%"
                    )

        # =================================================
        # MATCH SCORE CHART
        # =================================================

        st.markdown(
            '<div class="section-title">📈 Match Score Visualization</div>',
            unsafe_allow_html=True
        )

        if not job_results.empty:

            chart_data = job_results.copy()

            chart_data = chart_data.set_index(
                "Job Role"
            )

            st.bar_chart(
                chart_data["Match Score"],
                use_container_width=True
            )

        # =================================================
        # TARGET ROLE ANALYSIS
        # =================================================

        if target_role:

            st.markdown(
                '<div class="section-title">🎯 Target Role Analysis</div>',
                unsafe_allow_html=True
            )

            st.info(
                f"Highest matching role: **{target_role}**"
            )

            st.markdown(
                "### 📌 Required Skills"
            )

            if required_skills:

                st.write(
                    ", ".join(required_skills)
                )

        # =================================================
        # SKILL GAP ANALYSIS
        # =================================================

        st.markdown(
            '<div class="section-title">🔍 Skill Gap Analysis</div>',
            unsafe_allow_html=True
        )

        if target_role:

            st.write(
                f"Skills required for **{target_role}** "
                "that were not detected in the resume:"
            )

            if missing_skills:

                st.warning(
                    f"{len(missing_skills)} skill(s) "
                    "may need further development."
                )

                for skill in missing_skills:

                    st.write(
                        f"❌ {skill}"
                    )

            else:

                st.success(
                    "No missing skills were detected "
                    "from the current skill dictionary! 🎉"
                )

        # =================================================
        # LEARNING ROADMAP
        # =================================================

        st.markdown(
            '<div class="section-title">📚 Personalized Learning Roadmap</div>',
            unsafe_allow_html=True
        )

        if learning_roadmap:

            roadmap_df = pd.DataFrame(
                learning_roadmap
            )

            st.dataframe(
                roadmap_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "No additional learning roadmap is required "
                "based on the detected skills. 🎉"
            )

        # =================================================
        # PROJECT INFORMATION
        # =================================================

        st.markdown(
            '<div class="section-title">ℹ️ Analysis Information</div>',
            unsafe_allow_html=True
        )

        st.write(
            """
            **How the system works:**

            1. Resume is uploaded in PDF/DOCX format.
            2. Text is extracted from the resume.
            3. Extracted text is cleaned and normalized.
            4. Technical skills are identified.
            5. Resume is compared with job-role requirements.
            6. TF-IDF and cosine similarity are used for matching.
            7. Skill gaps are identified.
            8. A learning roadmap is generated.
            """
        )

        # =================================================
        # DISCLAIMER
        # =================================================

        st.divider()

        st.warning(
            """
            ⚠️ **Important:** Match scores are estimates based on
            resume content and predefined job-role requirements.

            This system is intended for career guidance and should
            not be used as an automatic hiring or rejection system.

            A missing keyword does not necessarily mean that the
            candidate lacks the underlying ability.
            """
        )

    except Exception as e:

        st.error(
            f"❌ An error occurred while processing the resume: {e}"
        )

else:

    # -----------------------------------------------------
    # BEFORE UPLOAD
    # -----------------------------------------------------

    st.info(
        "👆 Please upload a PDF or DOCX resume to start the analysis."
    )

    st.markdown(
        '<div class="section-title">✨ What This Application Does</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            ### 📄 Resume Analysis

            Extracts and cleans text
            from PDF and DOCX resumes.
            """
        )

    with col2:

        st.markdown(
            """
            ### 💼 Job Matching

            Compares resume content
            with multiple job roles.
            """
        )

    with col3:

        st.markdown(
            """
            ### 📚 Skill Roadmap

            Identifies skill gaps and
            provides learning guidance.
            """
        )