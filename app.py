import streamlit as st
from skills import *
import PyPDF2
# -------- Functions --------
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

def match_skills(resume_text, skills):
    found = []
    for skill in skills:
        if skill.lower() in resume_text:
            found.append(skill)
    return found

def calculate_score(found, total):
    if len(total) == 0:
        return 0
    return int((len(found) / len(total)) * 100)

# -------- UI --------
st.set_page_config(page_title="AI Resume Analyzer")
st.title("🤖 AI Resume Analyzer")

st.write("Upload your resume and check how well it matches a job role.")

role = st.selectbox("Select Job Role", ["Data Analyst", "ML Engineer","Data Scientist","Python Developer"])

uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    resume_text = extract_text(uploaded_file)

    # Select skills based on role
    if role == "Data Analyst":
        skills = data_analyst_skills

    elif role == "ML Engineer":
        skills = ml_skills

    elif role == "Data Scientist":
        skills = data_scientist_skills

    elif role == "Python Developer":
        skills = python_dev_skills

    # Now analyze
    found = match_skills(resume_text, skills)
    score = calculate_score(found, skills)
    missing = list(set(skills) - set(found))

    st.success("Resume analyzed successfully!")
    st.subheader(f"📊 Match Score: {score}%")
    st.progress(score / 100)
    st.write("✅ Skills Found:", found)
    st.write("❌ Missing Skills:", missing)

    if score < 70:
        st.warning("Improve missing skills to increase your chances.")

    st.info("Tip: Add relevant projects and tools to your resume.")