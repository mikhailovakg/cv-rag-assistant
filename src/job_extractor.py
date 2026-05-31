import requests
from bs4 import BeautifulSoup


def extract_job_text(url):

    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    return text