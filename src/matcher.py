"""Match resume skills against JD skills and generate improvement suggestions."""


def compute_match(resume_skills: list, jd_skills: list) -> dict:
    """Return a match summary dict."""
    resume_set = {s.lower() for s in resume_skills}
    jd_set = {s.lower() for s in jd_skills}

    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)
    extra = sorted(resume_set - jd_set)

    score = round(100 * len(matched) / len(jd_set)) if jd_set else 0

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "extra": extra,
    }


def generate_suggestions(match: dict, entities: dict) -> list:
    """Return a list of suggestion strings based on match results."""
    suggestions = []

    if match["missing"]:
        top_missing = match["missing"][:5]
        suggestions.append(
            f"**Address skill gaps.** The job description mentions "
            f"**{', '.join(top_missing)}** which weren't found in your resume. "
            f"If you have any experience with these, add them explicitly — even projects or coursework count."
        )

    if match["score"] < 50 and match["missing"]:
        suggestions.append(
            "**Tailor your summary.** Rewrite your resume summary/objective to mirror "
            "the language and top 3 keywords from the job description. "
            "Applicant Tracking Systems (ATS) match on keywords."
        )

    suggestions.append(
        "**Quantify your impact.** Replace vague phrases ('worked on X') with metrics "
        "('improved X by 30%', 'reduced load time from 4s to 0.8s'). Recruiters scan for numbers."
    )

    suggestions.append(
        "**Lead with strong action verbs.** Start each bullet with verbs like "
        "*Built, Led, Designed, Optimized, Reduced, Launched*. Avoid 'responsible for'."
    )

    if entities.get("PER"):
        suggestions.append(
            f"**Detected name:** *{entities['PER'][0]}* — confirm your contact details "
            "(email, phone, LinkedIn) sit prominently at the top of the resume."
        )

    if match["extra"]:
        suggestions.append(
            f"**Skills not needed for this role.** Consider de-emphasizing "
            f"**{', '.join(match['extra'][:3])}** on this version of your resume to keep focus on what matters."
        )

    return suggestions
