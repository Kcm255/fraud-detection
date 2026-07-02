"""
Configuration file for the Fraud Detection System.

All thresholds, scoring values, and constants are stored here.
This makes the project easy to maintain and modify.
"""

# ==========================================================
# FEATURE ENGINEERING CONFIGURATION
# ==========================================================

# Time window (in seconds) used for detecting repeated transactions
TRANSACTION_VELOCITY_WINDOW = 10

# Time window (in seconds) used for IP activity
IP_VELOCITY_WINDOW = 60

# Time window (in seconds) used for MAC activity
MAC_VELOCITY_WINDOW = 60

# Time window (in seconds) for detecting error bursts
ERROR_BURST_WINDOW = 30


# ==========================================================
# FEATURE THRESHOLDS
# ==========================================================

# Same transaction repeated this many times
TRANSACTION_VELOCITY_THRESHOLD = 3

# Requests from same IP within the IP window
IP_VELOCITY_THRESHOLD = 10

# Requests from same MAC within the MAC window
MAC_VELOCITY_THRESHOLD = 8

# Maximum retries before becoming suspicious
RETRY_THRESHOLD = 3

# Same error occurring repeatedly
ERROR_BURST_THRESHOLD = 5

# Same IP being used by multiple MAC addresses
MAX_MAC_PER_IP = 2

# Same MAC appearing from multiple IPs
MAX_IP_PER_MAC = 2

# Same transaction appearing from multiple devices
MAX_MAC_PER_TRANSACTION = 1

# Same transaction appearing from multiple IPs
MAX_IP_PER_TRANSACTION = 1


# ==========================================================
# RISK SCORING
# ==========================================================

DUPLICATE_TRANSACTION_SCORE = 30

TRANSACTION_VELOCITY_SCORE = 30

IP_VELOCITY_SCORE = 20

MAC_VELOCITY_SCORE = 20

MULTIPLE_MAC_TRANSACTION_SCORE = 30

MULTIPLE_IP_TRANSACTION_SCORE = 25

MULTIPLE_MAC_PER_IP_SCORE = 20

MULTIPLE_IP_PER_MAC_SCORE = 15

ERROR_BURST_SCORE = 15

RETRY_SCORE = 15
# Maximum possible risk score
MAX_RISK_SCORE = 100

# Minimum possible risk score
MIN_RISK_SCORE = 0


# ==========================================================
# FINAL CLASSIFICATION
# ==========================================================

PROPER_MAX_SCORE = 29

SUSPICIOUS_MAX_SCORE = 59

# Anything >= 60 is Fraud
FRAUD_MIN_SCORE = 60


# ==========================================================
# VALIDATION RULES
# ==========================================================

MIN_TRANSACTION_TIME = 0

ALLOW_EMPTY_ERROR_CODE = True

ALLOW_EMPTY_OPERATOR = True


# ==========================================================
# FILE PATHS
# ==========================================================

INPUT_FOLDER = "input_logs"

OUTPUT_FOLDER = "output"


# ==========================================================
# REPORT FILE NAMES
# ==========================================================

JSON_REPORT = "results.json"

CSV_REPORT = "results.csv"
# ==========================================================
# REQUIRED LOG FIELDS
# ==========================================================

# ==========================================================
# REQUIRED FIELDS
# ==========================================================

REQUIRED_FIELDS = [
    "timestamp",
    "Txn",
    "IP",
    "Mac",
    "CT",
    "DT",
    "ST",
    "TT"
]


NUMERIC_FIELDS = [
    "CT",
    "DT",
    "ST",
    "TT"
]