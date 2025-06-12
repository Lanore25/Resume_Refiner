import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="AI Resume Refiner", page_icon=":robot_face:", layout="centered")

st.title("AI Resume Refiner")
st.markdown("Upload your resume in PDF format and refine it using the power of AI!.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT format)", type=["pdf", "txt"])
job_description = st.text_input("Enter the job description")
job_role = st.text_input("Enter the job role you're taregtting(optional)")
analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text


def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    try:
        st.write("Analyzing your resume...")
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("The uploaded file is empty or could not be read.")
            st.stop()
        prompt = f"""Your objective is to generate a professional, compelling resume tailored to the provided {job_description}, maximizing interview chances by integrating best practices in content quality, keyword optimization, measurable achievements, and proper formatting.



If a tool, framework or skill doesn't match the ones mentioned in the {job_description} but a similar skill is mentioned, replace the tool/skill/framework with that keyword to match the {job_description}. For example, if Tableau is mentioned but the requirement asks for PowerBI, replace it with PowerBI. Be ethical, don't replace if it is not logical.



Guidelines to Follow:



Keyword and Skill Optimization:

Analyze the {job_description} and identify relevant keywords (hard and soft skills).

Match at least 80% of the job description’s keywords to align with applicant tracking systems (ATS).

Prioritize industry-relevant hard skills and soft skills in dedicated sections and throughout bullet points.

Incorporate Measurable Metrics:



Quantify achievements using the XYZ formula: Accomplished X, measured by Y, by doing Z.

Include at least five measurable results that clearly demonstrate impact.

Avoid vague statements; use metrics to highlight value and effectiveness.



Resume Length and Structure:

Keep the resume between 400-500 words for optimal readability and engagement.

Maintain a clean, organized structure with clear headings and bullet points.

Exceptions for roles requiring longer resumes (e.g., academia, federal jobs, C-suite) should be appropriately handled.

Content Quality and Language:



Eliminate buzzwords, clichés, and pronouns (e.g., “I,” “me,” “my”).

Use action-oriented, impactful language to emphasize accomplishments over duties.

Replace generic phrases with specific examples that showcase expertise and success.

Focus on selling professional experience, skills, and results, not merely summarizing past roles.

Additional Instructions:



Customize each section (Professional Summary, Experience, Skills, Education) to reflect relevance to the job.

Ensure consistent formatting, professional fonts, and appropriate use of whitespace.

Use concise bullet points, each starting with a strong action verb."""
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment in the Tech field."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        st.markdown("### Analysis Results")
        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occured: {str(e)}")