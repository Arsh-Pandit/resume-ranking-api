import re

SECTION_HEADERS = {
    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "skills & tools"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history"
    ],

    "education": [
        "education",
        "academic background",
        "academic qualifications",
        "educational background"
    ],

    "projects": [
        "projects",
        "personal projects",
        "academic projects"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "licenses",
        "professional certifications"
    ]
}


def normalize_line(line: str) -> str:
    """
    Normalize a line for header detection.
    """
    line = line.strip().lower()
    line = re.sub(r"[^a-z\s]", "", line)
    return line


def detect_section(line: str):
    """
    Check if a line corresponds to a known section header.
    """

    normalized = normalize_line(line)

    for section, headers in SECTION_HEADERS.items():
        for header in headers:
            if normalized == header:
                return section

    return None


def parse_resume_sections(text: str):
    """
    Parse resume text and split it into structured sections.
    """

    sections = {
        "skills": [],
        "experience": [],
        "education": [],
        "projects": [],
        "certifications": []
    }

    lines = text.split("\n")

    current_section = None

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        detected = detect_section(clean_line)

        if detected:
            current_section = detected
            continue

        if current_section:
            sections[current_section].append(clean_line)

    # convert lists to text
    for key in sections:
        sections[key] = " ".join(sections[key])

    return sections