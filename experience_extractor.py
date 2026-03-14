import re
from datetime import datetime


CURRENT_YEAR = datetime.now().year
CURRENT_MONTH = datetime.now().month


DATE_RANGE_PATTERN = re.compile(
    r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\s*(\d{4})\s*[-–]\s*(present|current|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\s*\d{4})",
    re.IGNORECASE
)


MONTH_MAP = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12
}


def parse_date(month_str, year_str):
    """
    Convert extracted month/year into numbers.
    """

    year = int(year_str)

    if month_str:
        month = MONTH_MAP.get(month_str.lower(), 1)
    else:
        month = 1

    return year, month


def calculate_experience(text):
    """
    Extract total years of experience from resume text.
    """

    matches = DATE_RANGE_PATTERN.findall(text)

    total_months = 0

    for match in matches:

        start_month, start_year, end_value, end_month, _ = match

        start_year, start_month = parse_date(start_month, start_year)

        if end_value.lower() in ["present", "current"]:
            end_year = CURRENT_YEAR
            end_month = CURRENT_MONTH
        else:
            end_year, end_month = parse_date(end_month, end_value.split()[-1])

        months = (end_year - start_year) * 12 + (end_month - start_month)

        if months > 0:
            total_months += months

    experience_years = total_months / 12

    return round(experience_years, 2)