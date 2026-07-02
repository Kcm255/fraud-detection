from config import (
    PROPER_MAX_SCORE,
    SUSPICIOUS_MAX_SCORE,
    FRAUD_MIN_SCORE
)


def classify_score(score):
    """
    Classify the final risk score.

    Returns:
        proper
        suspicious
        fraud
    """

    if score <= PROPER_MAX_SCORE:
        return "proper"

    elif score <= SUSPICIOUS_MAX_SCORE:
        return "suspicious"

    elif score >= FRAUD_MIN_SCORE:
        return "fraud"

    # Fallback (should never happen)
    return "unknown"