# engine/field_extractor.py

import re


def extract_fields(document_type, text):
    """
    Extract important fields from the OCR text.

    Parameters:
        document_type : application | aadhaar | pan
        text          : OCR extracted text

    Returns:
        Dictionary containing extracted fields.
    """

    text = clean_text(text)

    fields = {}

    # -----------------------------
    # Common Fields
    # -----------------------------

    fields["name"] = extract_name(text)
    fields["dob"] = extract_dob(text)

    # -----------------------------
    # Aadhaar
    # -----------------------------

    if document_type == "aadhaar":

        fields["aadhaar"] = extract_aadhaar(text)

    # -----------------------------
    # PAN
    # -----------------------------

    elif document_type == "pan":

        fields["pan"] = extract_pan(text)

    # -----------------------------
    # Application
    # -----------------------------

    elif document_type == "application":

        fields["aadhaar"] = extract_aadhaar(text)
        fields["pan"] = extract_pan(text)
        fields["mobile"] = extract_mobile(text)
        fields["email"] = extract_email(text)

    return fields


# ==========================================================
# Cleaning
# ==========================================================

def clean_text(text):
    """
    Remove extra spaces and blank lines.
    """

    text = text.replace("\r", "")

    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


# ==========================================================
# Name
# ==========================================================

def extract_name(text):
    """
    Extract name appearing after the word 'Name'.
    """

    lines = text.split("\n")

    for i, line in enumerate(lines):

        if "name" in line.lower():

            if i + 1 < len(lines):

                candidate = lines[i + 1].strip()

                if re.fullmatch(r"[A-Za-z ]{3,}", candidate):
                    return candidate

    return None


# ==========================================================
# DOB
# ==========================================================

def extract_dob(text):

    pattern = r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


# ==========================================================
# Aadhaar Number
# ==========================================================

def extract_aadhaar(text):

    pattern = r"\b\d{4}\s?\d{4}\s?\d{4}\b"

    match = re.search(pattern, text)

    if match:

        aadhaar = match.group()

        aadhaar = aadhaar.replace(" ", "")

        return aadhaar

    return None


# ==========================================================
# PAN Number
# ==========================================================

def extract_pan(text):

    pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


# ==========================================================
# Mobile Number
# ==========================================================

def extract_mobile(text):

    pattern = r"\b[6-9]\d{9}\b"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


# ==========================================================
# Email
# ==========================================================

def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None