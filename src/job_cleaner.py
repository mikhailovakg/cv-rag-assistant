def clean_job_text(text):

    lines = text.split()

    cleaned = []

    blacklist = {
        "cookie",
        "cookies",
        "privacy",
        "terms",
        "signin",
        "login"
    }

    for word in lines:

        if word.lower() not in blacklist:
            cleaned.append(word)

    return " ".join(cleaned)