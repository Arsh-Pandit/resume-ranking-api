import re


DEGREE_PATTERNS = {
    "btech": r"\b(b\.?\s?tech|bachelor of technology)\b",
    "be": r"\b(b\.?\s?e\.?|bachelor of engineering)\b",
    "bsc": r"\b(b\.?\s?sc|bachelor of science)\b",
    "mtech": r"\b(m\.?\s?tech|master of technology)\b",
    "msc": r"\b(m\.?\s?sc|master of science)\b",
    "mba": r"\b(mba|master of business administration)\b",
    "phd": r"\b(phd|doctor of philosophy)\b"
}


FIELD_PATTERN = re.compile(
    r"(computer science|information technology|artificial intelligence|data science|software engineering|computer engineering|electronics|electrical engineering)",
    re.IGNORECASE
)


def detect_degree(line):
    """
    Detect degree in a line.
    """

    for degree, pattern in DEGREE_PATTERNS.items():
        if re.search(pattern, line):
            return degree

    return None


def detect_field(line):
    """
    Detect field of study in a line.
    """

    match = FIELD_PATTERN.search(line)

    if match:
        return match.group(0).lower()

    return None


def extract_education(text):
    """
    Extract education information from education section text.
    """

    lines = [line.strip().lower() for line in text.split("\n") if line.strip()]

    education = []

    for i, line in enumerate(lines):

        degree = detect_degree(line)

        if degree:

            field = detect_field(line)

            # look at nearby lines for field
            if not field and i + 1 < len(lines):
                field = detect_field(lines[i + 1])

            if not field and i - 1 >= 0:
                field = detect_field(lines[i - 1])

            education.append({
                "degree": degree,
                "field": field
            })

    return education