"""Skill and entity extraction utilities."""
import re
from transformers import pipeline

# ----------- Curated skill taxonomy -----------
# Expand this list as needed; matching is case-insensitive whole-word.
SKILLS_LIST = [
    # Programming languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "ruby", "php",
    "kotlin", "swift", "scala", "r", "matlab", "perl",
    # Databases
    "sql", "nosql", "mongodb", "postgresql", "postgres", "mysql", "redis", "sqlite",
    "elasticsearch", "dynamodb", "cassandra",
    # Web frameworks
    "react", "angular", "vue", "next.js", "nuxt", "node.js", "express", "django",
    "flask", "fastapi", "spring", "spring boot", "laravel", "rails", "asp.net",
    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "github actions", "circleci", "gitlab ci",
    # Tools & methodology
    "git", "github", "gitlab", "bitbucket", "ci/cd", "agile", "scrum", "kanban",
    "jira", "confluence", "trello", "asana",
    # ML / AI
    "machine learning", "deep learning", "neural networks", "nlp",
    "natural language processing", "computer vision", "reinforcement learning",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "matplotlib",
    "seaborn", "plotly", "huggingface", "transformers", "bert", "gpt", "llm", "rag",
    "langchain", "llamaindex", "openai", "anthropic",
    # Data
    "data analysis", "data visualization", "data engineering", "etl", "data warehouse",
    "tableau", "power bi", "looker", "excel", "spark", "hadoop", "airflow", "dbt",
    "snowflake", "databricks", "redshift", "bigquery",
    # Web & systems
    "linux", "unix", "bash", "shell scripting", "rest api", "graphql", "soap",
    "microservices", "websockets", "grpc",
    # Frontend
    "html", "css", "sass", "tailwind", "bootstrap", "material ui", "figma",
    # Soft skills
    "communication", "teamwork", "leadership", "problem solving", "project management",
    "critical thinking", "time management",
]

# Cache the NER pipeline so we only load the model once per session
_ner_pipeline = None


def get_ner_pipeline():
    """Lazily load the HuggingFace NER model."""
    global _ner_pipeline
    if _ner_pipeline is None:
        _ner_pipeline = pipeline(
            "ner",
            model="dbmdz/bert-large-cased-finetuned-conll03-english",
            aggregation_strategy="simple",
        )
    return _ner_pipeline


def extract_skills(text: str) -> list:
    """Return a sorted list of skills found in `text` by whole-word match against SKILLS_LIST."""
    if not text:
        return []
    text_lower = text.lower()
    found = set()
    for skill in SKILLS_LIST:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, text_lower):
            found.add(skill)
    return sorted(found)


def extract_entities(text: str) -> dict:
    """Run NER on `text` and return entities grouped by type."""
    result = {"PER": [], "ORG": [], "LOC": [], "MISC": []}
    if not text:
        return result

    # Chunk to avoid BERT's 512-token limit (~1500 chars is safe)
    chunks = [text[i : i + 1500] for i in range(0, len(text), 1500)]
    ner = get_ner_pipeline()

    for chunk in chunks:
        try:
            entities = ner(chunk)
            for ent in entities:
                group = ent.get("entity_group", "MISC")
                word = ent["word"].strip()
                if (
                    group in result
                    and word not in result[group]
                    and len(word) > 1
                ):
                    result[group].append(word)
        except Exception:
            continue

    return result
