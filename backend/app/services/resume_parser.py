from os.path import split

import pymupdf


def extract_text_from_pdf(file_path: str) -> dict:
    document = pymupdf.open(file_path)

    total_characters = 0
    total_words = 0
    text = ""

    for page in document:
        page_text = page.get_text()

        text += page_text
        total_characters += len(page_text)
        total_words += len(page_text.split())

    document.close()

    return {
        "character_count": total_characters,
        "text": text,
        "total_words":total_words
    }