# engine/text_extractor.py

import os
import pdfplumber
import easyocr


_reader = None


def get_reader():
    """Create and cache the EasyOCR reader lazily."""
    global _reader

    if _reader is None:
        _reader = easyocr.Reader(['en'], gpu=False)

    return _reader


def extract_text(file_path):
    """
    Extract text from a PDF or image.

    Supported formats:
    - PDF
    - JPG
    - JPEG
    - PNG

    Returns:
        Extracted text as a string.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension in [".jpg", ".jpeg", ".png"]:
        return extract_image_text(file_path)

    else:
        raise ValueError(f"Unsupported file format: {extension}")


def extract_pdf_text(pdf_path):
    """
    Extract text from a text-based PDF.

    If the PDF is scanned, this function may return very little
    or no text. OCR support for scanned PDFs can be added later.
    """

    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

    return extracted_text.strip()


def extract_image_text(image_path):
    """
    Extract text from an image using EasyOCR.
    """

    reader = get_reader()
    result = reader.readtext(image_path, detail=0)

    extracted_text = "\n".join(result)

    return extracted_text.strip()