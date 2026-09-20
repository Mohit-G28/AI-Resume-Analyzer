from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfReader
from docx import Document
import io
import os

app = Flask(__name__)


# ==========================================
# SKILLS DATABASE
# ==========================================

SKILLS = [
    "python",
    "java",
    "c++",
    "c#",
    "javascript",
    "html",
    "css",
    "sql",
    "mysql",
    "mongodb",
    "flask",
    "django",
    "react",
    "node.js",
    "node",
    "php",
    "git",
    "github",
    "api",
    "rest api",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",
    "nlp",
    "data science",
    "pandas",
    "numpy",
    "matplotlib",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "excel",
    "power bi",
    "tableau",
    "communication",
    "problem solving",
    "teamwork",
    "leadership",
    "data structures",
    "dsa",
    "oop",
    "object oriented programming",
    "database",
    "dbms",
    "software development",
    "web development"
]


# ==========================================
# EXTRACT PDF TEXT
# ==========================================

def extract_text_from_pdf(file):

    text = ""

    try:
        reader = PdfReader(file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:

        print("PDF ERROR:", e)

    return text


# ==========================================
# EXTRACT DOCX TEXT
# ==========================================

def extract_text_from_docx(file):

    text = ""

    try:

        document = Document(file)

        for paragraph in document.paragraphs:

            if paragraph.text.strip():
                text += paragraph.text + "\n"

    except Exception as e:

        print("DOCX ERROR:", e)

    return text


# ==========================================
# EXTRACT RESUME TEXT
# ==========================================

def extract_resume_text(file):

    filename = file.filename.lower()

    file_data = file.read()

    file_stream = io.BytesIO(file_data)

    if filename.endswith(".pdf"):

        return extract_text_from_pdf(file_stream)

    elif filename.endswith(".docx"):

        return extract_text_from_docx(file_stream)

    return ""


# ==========================================
# DETECT SKILLS
# ==========================================

def detect_skills(text):

    text = text.lower()

    detected = []

    for skill in SKILLS:

        if skill.lower() in text:

            if skill not in detected:
                detected.append(skill)

    return detected


# ==========================================
# ATS SCORE
# ==========================================

def calculate_ats_score(text, skills):

    score = 0

    # Skill score
    skill_score = min(len(skills) * 5, 40)

    # Important sections
    sections = [
        "education",
        "experience",
        "skills",
        "project",
        "contact",
        "email"
    ]

    section_score = 0

    for section in sections:

        if section in text.lower():
            section_score += 5

    section_score = min(section_score, 30)

    # Resume length
    word_count = len(text.split())

    if word_count >= 300:

        length_score = 20

    elif word_count >= 150:

        length_score = 15

    elif word_count >= 80:

        length_score = 10

    else:

        length_score = 5

    # Basic formatting/content score
    formatting_score = 10

    score = (
        skill_score
        + section_score
        + length_score
        + formatting_score
    )

    return min(score, 100)


# ==========================================
# JOB MATCH
# ==========================================

def calculate_job_match(
    resume_text,
    job_description
):

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    if not job_description.strip():

        return 0, []

    job_skills = detect_skills(job_description)

    resume_skills = detect_skills(resume_text)

    if len(job_skills) == 0:

        return 0, []

    matched_skills = []

    for skill in job_skills:

        if skill in resume_skills:

            matched_skills.append(skill)

    matching_percentage = round(
        (
            len(matched_skills)
            / len(job_skills)
        ) * 100
    )

    return matching_percentage, matched_skills


# ==========================================
# MISSING SKILLS
# ==========================================

def get_missing_skills(
    job_description,
    resume_skills
):

    job_skills = detect_skills(job_description)

    missing = []

    for skill in job_skills:

        if skill not in resume_skills:

            missing.append(skill)

    return missing


# ==========================================
# SUGGESTIONS
# ==========================================

def generate_suggestions(
    ats_score,
    matching_percentage,
    missing_skills,
    resume_text
):

    suggestions = []

    resume_lower = resume_text.lower()

    if ats_score < 70:

        suggestions.append(
            "Improve your resume ATS compatibility by adding relevant skills and keywords."
        )

    if matching_percentage < 50:

        suggestions.append(
            "Add more skills related to the target job description."
        )

    if missing_skills:

        skills_text = ", ".join(
            missing_skills[:5]
        )

        suggestions.append(
            "Consider adding these relevant skills: "
            + skills_text
        )

    if "experience" not in resume_lower:

        suggestions.append(
            "Add your internship or work experience with measurable achievements."
        )

    if "project" not in resume_lower:

        suggestions.append(
            "Add relevant academic or personal projects."
        )

    if len(suggestions) == 0:

        suggestions.append(
            "Your resume has a good structure. Keep your skills and experience relevant to the target job."
        )

    return suggestions


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# ANALYZE PAGE
# ==========================================

@app.route("/analyze")
def analyze_page():

    return render_template("index.html")


# ==========================================
# ANALYZE RESUME API
# ==========================================

@app.route("/analyze", methods=["POST"])
def analyze_resume():

    try:

        # -------------------------------
        # GET FILE
        # -------------------------------

        resume_file = request.files.get("resume")

        if not resume_file:

            return jsonify({
                "success": False,
                "message": "Please upload your resume."
            })


        # -------------------------------
        # CHECK FILE TYPE
        # -------------------------------

        filename = resume_file.filename.lower()

        if not (
            filename.endswith(".pdf")
            or filename.endswith(".docx")
        ):

            return jsonify({
                "success": False,
                "message": "Only PDF and DOCX files are supported."
            })


        # -------------------------------
        # EXTRACT TEXT
        # -------------------------------

        resume_text = extract_resume_text(
            resume_file
        )

        if not resume_text.strip():

            return jsonify({
                "success": False,
                "message": "Could not read text from the resume."
            })


        # -------------------------------
        # JOB DESCRIPTION
        # -------------------------------

        job_description = (
            request.form.get("job_description")
            or request.form.get("jobDescription")
            or request.form.get("job")
            or ""
        )


        if not job_description.strip():

            return jsonify({
                "success": False,
                "message": "Please enter the job description."
            })


        # -------------------------------
        # DETECT SKILLS
        # -------------------------------

        resume_skills = detect_skills(
            resume_text
        )


        # -------------------------------
        # ATS SCORE
        # -------------------------------

        ats_score = calculate_ats_score(
            resume_text,
            resume_skills
        )


        # -------------------------------
        # JOB MATCH
        # -------------------------------

        matching_percentage, matched_skills = (
            calculate_job_match(
                resume_text,
                job_description
            )
        )


        # -------------------------------
        # MISSING SKILLS
        # -------------------------------

        missing_skills = get_missing_skills(
            job_description,
            resume_skills
        )


        # -------------------------------
        # SUGGESTIONS
        # -------------------------------

        suggestions = generate_suggestions(
            ats_score,
            matching_percentage,
            missing_skills,
            resume_text
        )


        # -------------------------------
        # FINAL RESULT
        # -------------------------------

        result = {

            "success": True,

            "ats_score": ats_score,

            "matching_percentage":
                matching_percentage,

            "skills":
                resume_skills,

            "matched_skills":
                matched_skills,

            "missing_skills":
                missing_skills,

            "suggestions":
                suggestions
        }


        # -------------------------------
        # TERMINAL OUTPUT
        # -------------------------------

        print("\n==============================")
        print("AI RESUME ANALYZER")
        print("==============================")

        print("FILE:", resume_file.filename)
        print("ATS SCORE:", ats_score)
        print("JOB MATCH:", matching_percentage)
        print("SKILLS:", resume_skills)
        print("MATCHED:", matched_skills)
        print("MISSING:", missing_skills)
        print("SUGGESTIONS:", suggestions)

        print("==============================\n")


        return jsonify(result)


    except Exception as e:

        print("ERROR:", e)

        return jsonify({

            "success": False,

            "message":
                "Something went wrong while analyzing the resume."

        })


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )