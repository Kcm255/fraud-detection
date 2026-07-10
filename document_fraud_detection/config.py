# config.py

# ==========================================================
# Risk Scores
# ==========================================================

DATABASE_NOT_FOUND_SCORE = 100

AADHAAR_MISMATCH_SCORE = 60

PAN_MISMATCH_SCORE = 60

DOB_MISMATCH_SCORE = 40

NAME_MISMATCH_SCORE = 20


# ==========================================================
# Classification Thresholds
# ==========================================================

PROPER_THRESHOLD = 30

SUSPICIOUS_THRESHOLD = 60


# ==========================================================
# Supported Documents
# ==========================================================

SUPPORTED_DOCUMENTS = [
    "application",
    "aadhaar",
    "pan"
]