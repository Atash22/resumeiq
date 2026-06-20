# 🧠 ResumeIQ

AI Resume Analyzer & Job-Match Coach — final project for **AASD 4013 Agile Methodologies**, Group 3.

Upload a PDF resume, paste a job description, and get a match score, missing skills, and AI-generated improvement suggestions.

## ⚡ Quick start (5 minutes)

```bash
# 1. Clone the repo
git clone https://github.com/Atash22/resumeiq.git
cd resumeiq

# 2. Create a virtual environment
python -m venv venv
# Activate it:
#   macOS/Linux:
source venv/bin/activate
#   Windows:
venv\Scripts\activate

# 3. Install dependencies (~5 min, downloads BERT model on first run)
pip install -r requirements.txt

# 4. Launch the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

> **First-time model download:** ~1.3 GB for the BERT NER model. It only downloads once.

## 🗂️ Project structure

```
resumeiq/
├── app.py              # Streamlit UI entry point
├── requirements.txt
├── README.md
└── src/
    ├── extractor.py    # PDF parsing, NER, skill extraction
    └── matcher.py      # Match scoring + suggestion generation
```

## ✨ Features

- 📄 **PDF resume parsing** via `pdfplumber`
- 🏷️ **Named Entity Recognition** with `dbmdz/bert-large-cased-finetuned-conll03-english`
- 🧩 **Skill matching** against a curated taxonomy of 100+ technical and soft skills
- 📊 **Match scoring** with visual breakdown
- 💡 **AI-generated suggestions** to improve resume fit

## 👥 Team — Group 3

| Member | Role |
|--------|------|
| Atash Kakabayev | Scrum Master |
| Nitesh Talukdar | Product Owner |
| Kazim Ali | Developer |

## 📅 Sprints

- **Sprint 1** (Jun 8–14, 2026): Resume parsing & entity extraction
- **Sprint 2** (Jun 15–21, 2026): JD matching, suggestion engine, UI polish

## 🛠️ Tech stack

Python · Streamlit · pdfplumber · HuggingFace Transformers · PyTorch
