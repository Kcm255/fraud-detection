from datetime import datetime
import ipaddress
import re

from config import REQUIRED_FIELDS, NUMERIC_FIELDS


def is_valid_timestamp(timestamp):
    """
    Checks whether the timestamp follows the expected format.

    Example:
    22/Apr/2026 14:39:50,110
    """
    try:
        datetime.strptime(timestamp, "%d/%b/%Y %H:%M:%S,%f")
        return True
    except ValueError:
        return False


def is_valid_ip(ip):
    """
    Checks whether an IP address is valid.
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_mac(mac):
    """
    Checks whether a MAC address is valid.

    Example:
    AA:BB:CC:DD:EE:FF
    """
    pattern = r"^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$"
    return re.match(pattern, mac) is not None


def validate_records(records):
    """
    Validates all log records.

    Returns:
        valid_records
        invalid_records
    """

    valid_records = []
    invalid_records = []

    for record in records:

        errors = []

        # ---------------------------------
        # Required Fields
        # ---------------------------------

        for field in REQUIRED_FIELDS:
            if field not in record:
                errors.append(f"Missing field: {field}")

        # ---------------------------------
        # Empty Mandatory Fields
        # ---------------------------------

        if record.get("Txn", "") == "":
            errors.append("Empty Transaction ID")

        if record.get("IP", "") == "":
            errors.append("Empty IP Address")

        if record.get("Mac", "") == "":
            errors.append("Empty MAC Address")

        # ---------------------------------
        # Numeric Validation
        # ---------------------------------

        for field in NUMERIC_FIELDS:

            value = record.get(field)

            if not isinstance(value, (int, float)):
                errors.append(f"{field} must be numeric")

        # ---------------------------------
        # Timestamp Validation
        # ---------------------------------

        timestamp = record.get("timestamp")

        if timestamp and not is_valid_timestamp(timestamp):
            errors.append("Invalid timestamp format")

        # ---------------------------------
        # IP Validation
        # ---------------------------------

        ip = record.get("IP")

        if ip and not is_valid_ip(ip):
            errors.append("Invalid IP address")

        # ---------------------------------
        # MAC Validation
        # ---------------------------------

        mac = record.get("Mac")

        if mac and not is_valid_mac(mac):
            errors.append("Invalid MAC address")

        # ---------------------------------
        # Business Rule Validation
        # ---------------------------------

        tt = record.get("TT")
        dt = record.get("DT")
        st = record.get("ST")

        if isinstance(tt, (int, float)) and tt < 0:
            errors.append("TT cannot be negative")

        if (
            isinstance(dt, (int, float))
            and isinstance(st, (int, float))
            and dt < st
        ):
            errors.append("DT cannot be less than ST")

        # ---------------------------------
        # Final Decision
        # ---------------------------------

        if errors:
            invalid_records.append({
                "record": record,
                "errors": errors
            })
        else:
            valid_records.append(record)

    return valid_records, invalid_records