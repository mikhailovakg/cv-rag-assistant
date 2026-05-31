def build_job_match_prompt(
    cv_context,
    job_description
):
    return f"""
You are an experienced recruiter and career coach.

Compare the candidate CV against the job description.

Provide:

# Match Score
Estimate a score between 0 and 100.

# Strengths
List matching qualifications.

# Missing Skills
List important missing skills or experiences.

# Recommendations
Suggest improvements to increase suitability.

# Overall Assessment
Provide a concise assessment.

CV Information:
{cv_context}

Job Description:
{job_description}
"""