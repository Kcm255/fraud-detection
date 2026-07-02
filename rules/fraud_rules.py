from config import (
    DUPLICATE_TRANSACTION_SCORE,
    TRANSACTION_VELOCITY_SCORE,
    IP_VELOCITY_SCORE,
    MAC_VELOCITY_SCORE,
    MULTIPLE_MAC_TRANSACTION_SCORE,
    MULTIPLE_IP_TRANSACTION_SCORE,
    MULTIPLE_MAC_PER_IP_SCORE,
    MULTIPLE_IP_PER_MAC_SCORE,
    ERROR_BURST_SCORE,
    RETRY_SCORE,
    TRANSACTION_VELOCITY_THRESHOLD,
    IP_VELOCITY_THRESHOLD,
    MAC_VELOCITY_THRESHOLD,
    RETRY_THRESHOLD,
    ERROR_BURST_THRESHOLD,
    MAX_MAC_PER_TRANSACTION,
    MAX_IP_PER_TRANSACTION,
    MAX_MAC_PER_IP,
    MAX_IP_PER_MAC,
)


def check_duplicate_transaction(txn, features):
    if features["txn_counts"].get(txn, 0) > 1:
        return DUPLICATE_TRANSACTION_SCORE, "Duplicate Transaction"

    return 0, None


def check_transaction_velocity(txn, features):
    velocity = features["transaction_velocity"].get(txn)

    if velocity and velocity["max_requests"] >= TRANSACTION_VELOCITY_THRESHOLD:
        return TRANSACTION_VELOCITY_SCORE, "High Transaction Velocity"

    return 0, None


def check_ip_velocity(ip, features):
    velocity = features["ip_velocity"].get(ip)

    if velocity and velocity["max_requests"] >= IP_VELOCITY_THRESHOLD:
        return IP_VELOCITY_SCORE, "High IP Velocity"

    return 0, None


def check_mac_velocity(mac, features):
    velocity = features["mac_velocity"].get(mac)

    if velocity and velocity["max_requests"] >= MAC_VELOCITY_THRESHOLD:
        return MAC_VELOCITY_SCORE, "High MAC Velocity"

    return 0, None


def check_multiple_devices(txn, features):
    txn_devices = features["txn_to_mac"].get(txn, [])

    if len(txn_devices) > MAX_MAC_PER_TRANSACTION:
        return MULTIPLE_MAC_TRANSACTION_SCORE, "Transaction Used on Multiple Devices"

    return 0, None


def check_multiple_ips(txn, features):
    txn_ips = features["txn_to_ip"].get(txn, [])

    if len(txn_ips) > MAX_IP_PER_TRANSACTION:
        return MULTIPLE_IP_TRANSACTION_SCORE, "Transaction Used from Multiple IPs"

    return 0, None


def check_ip_device_mapping(ip, features):
    devices = features["ip_to_mac"].get(ip, [])

    if len(devices) > MAX_MAC_PER_IP:
        return MULTIPLE_MAC_PER_IP_SCORE, "Multiple Devices Using Same IP"

    return 0, None


def check_device_ip_mapping(mac, features):
    ips = features["mac_to_ip"].get(mac, [])

    if len(ips) > MAX_IP_PER_MAC:
        return MULTIPLE_IP_PER_MAC_SCORE, "Device Used on Multiple IPs"

    return 0, None


def check_retry_detection(txn, features):
    retries = features["retry_counts"].get(txn, 0)

    if retries >= RETRY_THRESHOLD:
        return RETRY_SCORE, "Repeated Failed Attempts"

    return 0, None


def check_error_burst(err, features):
    if err:
        error_velocity = features["error_velocity"].get(err)

        if error_velocity and error_velocity["max_requests"] >= ERROR_BURST_THRESHOLD:
            return ERROR_BURST_SCORE, "Error Burst Detected"

    return 0, None


def evaluate_record(record, features):
    """
    Evaluates a single record against all fraud rules.

    Returns:
        {
            "risk_score": int,
            "reasons": list
        }
    """

    score = 0
    reasons = []

    txn = record.get("Txn")
    ip = record.get("IP")
    mac = record.get("Mac")
    err = record.get("Err")

    rules = [
        check_duplicate_transaction(txn, features),
        check_transaction_velocity(txn, features),
        check_ip_velocity(ip, features),
        check_mac_velocity(mac, features),
        check_multiple_devices(txn, features),
        check_multiple_ips(txn, features),
        check_ip_device_mapping(ip, features),
        check_device_ip_mapping(mac, features),
        check_retry_detection(txn, features),
        check_error_burst(err, features),
    ]

    for points, reason in rules:
        score += points

        if reason:
            reasons.append(reason)

    return {
        "risk_score": score,
        "reasons": reasons,
    }