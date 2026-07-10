# rules/document_rules.py

from config import (
    DATABASE_NOT_FOUND_SCORE,
    AADHAAR_MISMATCH_SCORE,
    PAN_MISMATCH_SCORE,
    DOB_MISMATCH_SCORE,
    NAME_MISMATCH_SCORE
)


def evaluate_document(comparison):
    """
    Calculate fraud risk score.

    Input:
        comparison dictionary

    Output:
        {
            risk_score,
            reasons
        }
    """

    risk_score = 0

    reasons = []

    # ----------------------------------------------------
    # Record Not Found
    # ----------------------------------------------------

    if not comparison["record_found"]:

        risk_score += DATABASE_NOT_FOUND_SCORE

        reasons.append("User Record Not Found")

        return {
            "risk_score": risk_score,
            "reasons": reasons
        }

    # ----------------------------------------------------
    # Name
    # ----------------------------------------------------

    if not comparison["name_match"]:

        risk_score += NAME_MISMATCH_SCORE

        reasons.append("Name Mismatch")

    # ----------------------------------------------------
    # DOB
    # ----------------------------------------------------

    if not comparison["dob_match"]:

        risk_score += DOB_MISMATCH_SCORE

        reasons.append("DOB Mismatch")

    # ----------------------------------------------------
    # Aadhaar
    # ----------------------------------------------------

    if comparison["aadhaar_match"] is False:

        risk_score += AADHAAR_MISMATCH_SCORE

        reasons.append("Aadhaar Mismatch")

    # ----------------------------------------------------
    # PAN
    # ----------------------------------------------------

    if comparison["pan_match"] is False:

        risk_score += PAN_MISMATCH_SCORE

        reasons.append("PAN Mismatch")

    return {
        "risk_score": risk_score,
        "reasons": reasons
    }