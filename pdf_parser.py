import fitz
import re


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s@.+#\-]", " ", text)
    text = text.lower()
    return text.strip()


def extract_text_from_pdf(file_bytes: bytes) -> str:

    text_pages = []

    with fitz.open(stream=file_bytes, filetype="pdf") as pdf:

        for page in pdf:
            page_text = page.get_text("text")
            if page_text:
                text_pages.append(page_text)

    full_text = "\n".join(text_pages)
    cleaned_text = clean_text(full_text)
    return cleaned_text