"""ResumeIQ - AI Resume Analyzer & Job-Match Coach
AASD 4013 Agile Methodologies - Group 4
"""
import streamlit as st
import pdfplumber
from src.extractor import extract_skills, extract_entities
from src.matcher import compute_match, generate_suggestions

# ----------------- Page config -----------------
st.set_page_config(
    page_title="ResumeIQ",
    page_icon="🧠",
    layout="wide",
)

# ----------------- Header -----------------
st.title("🧠 ResumeIQ")
st.caption("AI Resume Analyzer & Job-Match Coach · Built by Group 4 · AASD 4013")
st.divider()

# ----------------- Inputs (two columns) -----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Your Resume")
    pdf_file = st.file_uploader(
        "Upload a PDF resume",
        type="pdf",
        help="Text-based PDFs only — scanned images won't work.",
    )
    resume_text = ""
    if pdf_file:
        try:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        resume_text += page_text + "\n"
            st.success(f"✓ Parsed {len(resume_text)} characters from {len(pdf.pages)} page(s)")
            with st.expander("Preview extracted text"):
                st.text(resume_text[:1500] + ("..." if len(resume_text) > 1500 else ""))
        except Exception as e:
            st.error(f"Could not parse PDF: {e}")

with col2:
    st.subheader("💼 Job Description")
    jd_text = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="e.g. We're looking for a Data Analyst with experience in Python, SQL, Tableau...",
    )

# ----------------- Analyze button -----------------
st.divider()
analyze = st.button(
    "🔍 Analyze Match",
    type="primary",
    disabled=(not resume_text or not jd_text),
    use_container_width=True,
)

# ----------------- Results -----------------
if analyze:
    with st.spinner("Extracting skills and analyzing match..."):
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)
        entities = extract_entities(resume_text)
        match = compute_match(resume_skills, jd_skills)
        suggestions = generate_suggestions(match, entities)

    # Top metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Match Score", f"{match['score']}%")
    m2.metric("Matched Skills", len(match["matched"]))
    m3.metric("Missing Skills", len(match["missing"]))

    st.progress(match["score"] / 100)

    if match["score"] >= 70:
        st.success("Strong match! Your resume aligns well with this job.")
    elif match["score"] >= 40:
        st.warning("Moderate match. Several gaps to address.")
    else:
        st.error("Low match. Consider whether this role fits, or invest in upskilling.")

    # Detail tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["✅ Matched Skills", "⚠️ Missing Skills", "💡 Suggestions", "🔬 Extracted Entities"]
    )

    with tab1:
        if match["matched"]:
            st.write(f"**{len(match['matched'])} skills from the job description are present in your resume:**")
            cols = st.columns(3)
            for i, skill in enumerate(match["matched"]):
                cols[i % 3].success(f"✓ {skill}")
        else:
            st.info("No overlapping skills detected yet.")

    with tab2:
        if match["missing"]:
            st.write(f"**{len(match['missing'])} skills mentioned in the job description aren't in your resume:**")
            cols = st.columns(3)
            for i, skill in enumerate(match["missing"]):
                cols[i % 3].warning(f"○ {skill}")
        else:
            st.success("Your resume covers all skills mentioned in the JD!")

    with tab3:
        st.write("### 💡 Improvement Suggestions")
        for i, s in enumerate(suggestions, 1):
            st.write(f"**{i}.** {s}")

    with tab4:
        st.write("**Named entities detected in your resume:**")
        c1, c2, c3 = st.columns(3)
        c1.write("**👤 People (PER)**")
        c1.write(entities.get("PER", []) or "—")
        c2.write("**🏢 Organizations (ORG)**")
        c2.write(entities.get("ORG", []) or "—")
        c3.write("**📍 Locations (LOC)**")
        c3.write(entities.get("LOC", []) or "—")

# ----------------- Footer -----------------
st.divider()
st.caption(
    "ResumeIQ is a course project for AASD 4013 Agile Methodologies. "
    "Results are advisory only — always tailor your resume manually before submitting."
)
