import re
from skills import SKILLS


def normalize_text(text: str) -> str:

    text = text.lower()
    text = re.sub(r"[\/,|]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def extract_skills(text: str):

    text = normalize_text(text)
    found_skills = set()

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.add(skill)

    return sorted(list(found_skills))