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


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

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
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 27px;
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

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
    "Analyze your resume, discover relevant job roles, "
    "identify skill gaps, and get a personalized learning roadmap."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ About the Project")

    st.write(
        """
        This application analyzes resume content using
        Natural Language Processing and Machine Learning
        techniques.
        """
    )

    st.markdown("### 🔧 Technologies")

    st.write(
        """
        - Python
        - Streamlit
        - Pandas
        - NumPy
        - Scikit-learn
        - TF-IDF
        - Cosine Similarity
        - PyPDF
        - python-docx
        """
    )

    st.markdown("### ✨ Features")

    st.write(
        """
        ✅ PDF/DOCX Resume Upload

        ✅ Text Extraction

        ✅ Text Cleaning

        ✅ Skill Detection

        ✅ Job Matching

        ✅ Target Role Selection

        ✅ Skill Gap Analysis

        ✅ Learning Roadmap
        """
    )


# =========================================================
# RESUME UPLOAD
# =========================================================

st.markdown(
    '<div class="section-title">📤 Upload Your Resume</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"],
    help="Upload your resume in PDF or DOCX format."
)


# =========================================================
# MAIN APPLICATION
# =========================================================

if uploaded_file is not None:

    st.success(
        f"Resume uploaded successfully: {uploaded_file.name} ✅"
    )

    try:

        # =================================================
        # 1. TEXT EXTRACTION
        # =================================================

        resume_text = extract_resume_text(
            uploaded_file
        )

        # =================================================
        # 2. TEXT CLEANING
        # =================================================

        cleaned_text = clean_resume_text(
            resume_text
        )

        # =================================================
        # 3. SKILL EXTRACTION
        # =================================================

        found_skills = extract_skills(
            cleaned_text
        )

        total_skills = sum(
            len(skills)
            for skills in found_skills.values()
        )

        # =================================================
        # 4. JOB ROLE MATCHING
        # =================================================

        job_results = match_resume_to_jobs(
            cleaned_text
        )

        # =================================================
        # SUMMARY METRICS
        # =================================================

        st.markdown(
            '<div class="section-title">📊 Resume Analysis Summary</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🧠 Skills Detected",
                total_skills
            )

        with col2:

            if not job_results.empty:

                highest_score = job_results.iloc[0]["Match Score"]

                st.metric(
                    "📈 Highest Match",
                    f"{highest_score:.2f}%"
                )

            else:

                st.metric(
                    "📈 Highest Match",
                    "N/A"
                )

        with col3:

            st.metric(
                "💼 Job Roles",
                len(job_results)
            )

        with col4:

            st.metric(
                "🔍 Skill Gaps",
                "Select Role"
            )


        # =================================================
        # EXTRACTED RESUME TEXT
        # =================================================

        st.markdown(
            '<div class="section-title">📄 Resume Text Analysis</div>',
            unsafe_allow_html=True
        )

        if cleaned_text.strip():

            with st.expander(
                "🔎 View Extracted & Cleaned Resume Text"
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
        # SKILL DETECTION
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

                st.write(
                    skill_text
                )

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
            "The resume is compared with predefined job roles "
            "using TF-IDF and cosine similarity."
        )

        if not job_results.empty:

            display_results = job_results.copy()

            display_results["Match Score"] = (
                display_results["Match Score"]
                .map(lambda x: f"{x:.2f}%")
            )

            st.dataframe(
                display_results,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No job-role matching results available."
            )


        # =================================================
        # TOP 3 JOB ROLES
        # =================================================

        st.markdown(
            '<div class="section-title">🏆 Top 3 Matching Job Roles</div>',
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
                range(1, len(top_3) + 1)
            )

            st.dataframe(
                top_3,
                use_container_width=True,
                hide_index=True
            )

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
        # TARGET JOB ROLE SELECTION
        # =================================================

        st.markdown(
            '<div class="section-title">🎯 Select Your Target Job Role</div>',
            unsafe_allow_html=True
        )

        if not job_results.empty:

            role_options = job_results["Job Role"].tolist()

            default_role = job_results.iloc[0]["Job Role"]

            target_role = st.selectbox(
                "Choose the job role you want to analyze:",
                role_options,
                index=role_options.index(default_role)
            )

            st.info(
                f"🎯 Selected Target Role: **{target_role}**"
            )


            # =============================================
            # SELECTED ROLE SCORE
            # =============================================

            selected_row = job_results[
                job_results["Job Role"] == target_role
            ]

            if not selected_row.empty:

                selected_score = selected_row.iloc[0][
                    "Match Score"
                ]

                st.metric(
                    "Target Role Match Score",
                    f"{selected_score:.2f}%"
                )


            # =============================================
            # REQUIRED SKILLS
            # =============================================

            required_skills = get_required_skills(
                target_role
            )

            st.markdown(
                "### 📌 Required Skills"
            )

            if required_skills:

                st.write(
                    ", ".join(required_skills)
                )

            else:

                st.info(
                    "No required skills found."
                )


            # =============================================
            # SKILL GAP ANALYSIS
            # =============================================

            missing_skills = find_missing_skills(
                found_skills,
                required_skills
            )

            st.markdown(
                "### 🔍 Skill Gap Analysis"
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


            # =============================================
            # LEARNING ROADMAP
            # =============================================

            st.markdown(
                "### 📚 Personalized Learning Roadmap"
            )

            learning_roadmap = generate_learning_roadmap(
                missing_skills
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
        # HOW THE SYSTEM WORKS
        # =================================================

        st.markdown(
            '<div class="section-title">🔄 How the System Works</div>',
            unsafe_allow_html=True
        )

        st.write(
            """
            **Step 1:** Upload a PDF or DOCX resume.

            **Step 2:** Extract text from the uploaded resume.

            **Step 3:** Clean and normalize the extracted text.

            **Step 4:** Detect technical skills using a predefined
            skill dictionary.

            **Step 5:** Compare the resume with predefined job roles.

            **Step 6:** Calculate similarity using TF-IDF and
            cosine similarity.

            **Step 7:** Display job-role match scores and top
            matching roles.

            **Step 8:** Select a target job role.

            **Step 9:** Identify missing skills.

            **Step 10:** Generate a personalized learning roadmap.
            """
        )


        # =================================================
        # RESPONSIBLE AI
        # =================================================

        st.divider()

        st.warning(
            """
            ⚠️ **Responsible AI Notice**

            Match scores are estimates based on resume content
            and predefined job-role requirements.

            This application is intended for career guidance and
            should not be used as an automatic hiring or rejection
            system.

            A missing keyword does not necessarily mean that a
            candidate lacks the underlying ability.
            """
        )


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        st.error(
            f"❌ An error occurred while processing the resume: {e}"
        )


# =========================================================
# BEFORE RESUME UPLOAD
# =========================================================

else:

    st.info(
        "👆 Please upload a PDF or DOCX resume to start the analysis."
    )

    st.markdown(
        '<div class="section-title">✨ Application Features</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            ### 📄 Resume Analysis

            Extract and clean resume text
            from PDF and DOCX files.
            """
        )

    with col2:

        st.markdown(
            """
            ### 💼 Job Matching

            Compare your resume with
            multiple job roles.
            """
        )

    with col3:

        st.markdown(
            """
            ### 📚 Career Roadmap

            Identify skill gaps and
            generate learning guidance.
            """
        )