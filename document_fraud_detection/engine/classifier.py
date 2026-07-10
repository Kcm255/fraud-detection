# engine/classifier.py

from config import (
    PROPER_THRESHOLD,
    SUSPICIOUS_THRESHOLD
)


def classify_score(score):

    if score < PROPER_THRESHOLD:
        return "Proper"

    elif score < SUSPICIOUS_THRESHOLD:
        return "Suspicious"

    else:
        return "Fraud"