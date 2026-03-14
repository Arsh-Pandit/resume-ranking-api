import json
import re
from pathlib import Path


SKILLS_PATH = Path("D:\Resume_Screening\data\skills.json")
ALIASES_PATH = Path("D:\Resume_Screening\data\skill_aliases.json")


def load_skills():
    """
    Load and flatten skills from skills.json
    """

    with open(SKILLS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    skills = []

    for category in data.values():
        skills.extend(category)

    skills = list(set(skill.lower() for skill in skills))

    return skills


def load_aliases():
    """
    Convert:
    canonical -> [aliases]

    into:
    alias -> canonical
    """

    with open(ALIASES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    alias_map = {}

    for canonical, alias_list in data.items():

        canonical = canonical.lower()

        alias_map[canonical] = canonical

        for alias in alias_list:
            alias_map[alias.lower()] = canonical

    return alias_map


def compile_skill_patterns(skills):
    """
    Compile regex patterns for each skill.
    """

    patterns = []

    for skill in skills:
        pattern = re.compile(r"\b" + re.escape(skill) + r"\b")
        patterns.append((skill, pattern))

    return patterns


def compile_alias_patterns(alias_map):
    """
    Compile regex patterns for alias replacement.
    """

    patterns = []

    for alias, canonical in alias_map.items():
        pattern = re.compile(r"\b" + re.escape(alias) + r"\b")
        patterns.append((pattern, canonical))

    return patterns


# Load data once
SKILLS = load_skills()
ALIASES = load_aliases()

# Compile regex once
SKILL_PATTERNS = compile_skill_patterns(SKILLS)
ALIAS_PATTERNS = compile_alias_patterns(ALIASES)


def normalize_text(text):
    """
    Normalize resume text
    """

    text = text.lower()

    text = re.sub(r"[\/,|]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text


def apply_aliases(text):
    """
    Replace aliases with canonical skill names
    """

    for pattern, replacement in ALIAS_PATTERNS:
        text = pattern.sub(replacement, text)

    return text


def extract_skills(text):
    """
    Extract skills from resume text
    """

    text = normalize_text(text)

    text = apply_aliases(text)

    found_skills = set()

    for skill, pattern in SKILL_PATTERNS:
        if pattern.search(text):
            found_skills.add(skill)

    return sorted(found_skills)