from collections import Counter, defaultdict
from datetime import datetime

from config import (
    TRANSACTION_VELOCITY_WINDOW,
    IP_VELOCITY_WINDOW,
    MAC_VELOCITY_WINDOW,
    ERROR_BURST_WINDOW,
)


def parse_timestamp(timestamp):
    """
    Convert timestamp string into a datetime object.
    Example:
    22/Apr/2026 14:39:50,110
    """

    return datetime.strptime(timestamp, "%d/%b/%Y %H:%M:%S,%f")


def calculate_velocity(records, key_name, window_seconds):
    """
    Generic velocity calculator.

    Example:
        key_name = "Txn"
        key_name = "IP"
        key_name = "Mac"

    Returns:

    {
        key:
        {
            "max_requests": value,
            "window_seconds": value
        }
    }
    """

    grouped = defaultdict(list)

    # Group timestamps
    for record in records:

        key = record.get(key_name)
        timestamp = record.get("timestamp")

        if key and timestamp:
            grouped[key].append(parse_timestamp(timestamp))

    velocity = {}

    # Sliding Window
    for key, timestamps in grouped.items():

        timestamps.sort()

        left = 0
        max_requests = 0

        for right in range(len(timestamps)):

            while (
                timestamps[right] - timestamps[left]
            ).total_seconds() > window_seconds:

                left += 1

            current_requests = right - left + 1

            max_requests = max(max_requests, current_requests)

        velocity[key] = {
            "max_requests": max_requests,
            "window_seconds": window_seconds
        }

    return velocity

def calculate_retry_counts(records):
    """
    Counts how many failed attempts occurred
    for each transaction.
    """

    retry_counts = Counter()

    for record in records:

        txn = record.get("Txn")
        err = record.get("Err")

        # Any non-empty error means failure
        if txn and err:
            retry_counts[txn] += 1

    return dict(retry_counts)

def extract_features(records):
    """
    Extract all features from validated records.
    """

    # -------------------------
    # Frequency Counters
    # -------------------------

    txn_counts = Counter()
    ip_counts = Counter()
    mac_counts = Counter()
    error_counts = Counter()

    # -------------------------
    # Relationship Mapping
    # -------------------------

    ip_to_mac = defaultdict(set)
    mac_to_ip = defaultdict(set)

    txn_to_ip = defaultdict(set)
    txn_to_mac = defaultdict(set)

    # -------------------------
    # Process Every Record
    # -------------------------

    for record in records:

        txn = record.get("Txn")
        ip = record.get("IP")
        mac = record.get("Mac")
        err = record.get("Err")

        # Frequency
        if txn:
            txn_counts[txn] += 1

        if ip:
            ip_counts[ip] += 1

        if mac:
            mac_counts[mac] += 1

        if err:
            error_counts[err] += 1

        # Relationship Mapping
        if ip and mac:
            ip_to_mac[ip].add(mac)
            mac_to_ip[mac].add(ip)

        if txn and ip:
            txn_to_ip[txn].add(ip)

        if txn and mac:
            txn_to_mac[txn].add(mac)

    # -------------------------
    # Velocity Features
    # -------------------------

    transaction_velocity = calculate_velocity(
        records,
        "Txn",
        TRANSACTION_VELOCITY_WINDOW
    )

    ip_velocity = calculate_velocity(
        records,
        "IP",
        IP_VELOCITY_WINDOW
    )

    mac_velocity = calculate_velocity(
        records,
        "Mac",
        MAC_VELOCITY_WINDOW
    )

    error_velocity = calculate_velocity(
        records,
        "Err",
        ERROR_BURST_WINDOW
    )

    retry_counts = calculate_retry_counts(records)

    # -------------------------
    # Store Features
    # -------------------------

    features = {

        "txn_counts": dict(txn_counts),

        "ip_counts": dict(ip_counts),

        "mac_counts": dict(mac_counts),

        "error_counts": dict(error_counts),

        "ip_to_mac": {
            k: list(v)
            for k, v in ip_to_mac.items()
        },

        "mac_to_ip": {
            k: list(v)
            for k, v in mac_to_ip.items()
        },

        "txn_to_ip": {
            k: list(v)
            for k, v in txn_to_ip.items()
        },

        "txn_to_mac": {
            k: list(v)
            for k, v in txn_to_mac.items()
        },

        "transaction_velocity": transaction_velocity,

        "ip_velocity": ip_velocity,

        "mac_velocity": mac_velocity,

        "error_velocity": error_velocity,

        "retry_counts": retry_counts,

    }

    return features