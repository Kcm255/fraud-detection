# engine/validator.py

import re


def validate_document(document_type, fields):
    """
    Validate extracted document fields.

    Parameters:
        document_type : application | aadhaar | pan
        fields        : dictionary returned by field_extractor

    Returns:
        {
            "valid": True/False,
            "errors": [...]
        }
    """

    errors = []

    # =====================================================
    # Common Validation
    # =====================================================

    if not fields.get("name"):
        errors.append("Missing Name")

    if not fields.get("dob"):
        errors.append("Missing Date of Birth")

    # =====================================================
    # Aadhaar Validation
    # =====================================================

    if document_type == "aadhaar":

        aadhaar = fields.get("aadhaar")

        if not aadhaar:
            errors.append("Missing Aadhaar Number")

        elif not validate_aadhaar(aadhaar):
            errors.append("Invalid Aadhaar Number")

    # =====================================================
    # PAN Validation
    # =====================================================

    elif document_type == "pan":

        pan = fields.get("pan")

        if not pan:
            errors.append("Missing PAN Number")

        elif not validate_pan(pan):
            errors.append("Invalid PAN Number")

    # =====================================================
    # Application Validation
    # =====================================================

    elif document_type == "application":

        aadhaar = fields.get("aadhaar")
        pan = fields.get("pan")

        if not aadhaar:
            errors.append("Missing Aadhaar Number")

        elif not validate_aadhaar(aadhaar):
            errors.append("Invalid Aadhaar Number")

        if not pan:
            errors.append("Missing PAN Number")

        elif not validate_pan(pan):
            errors.append("Invalid PAN Number")

    # =====================================================

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


# ==========================================================
# Aadhaar Validation
# ==========================================================

def validate_aadhaar(aadhaar):
    """
    Aadhaar should contain exactly 12 digits.
    """

    pattern = r"^\d{12}$"

    return re.fullmatch(pattern, aadhaar) is not None


# ==========================================================
# PAN Validation
# ==========================================================

def validate_pan(pan):
    """
    PAN Format

    ABCDE1234F
    """

    pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"

    return re.fullmatch(pattern, pan) is not None