# engine/comparator.py


def normalize_name(name):
    if not name:
        return ""

    return " ".join(name.strip().lower().split())


def normalize_dob(dob):
    if not dob:
        return ""

    dob = dob.replace("/", "-")
    dob = dob.replace(".", "-")

    return dob.strip()


def normalize_aadhaar(aadhaar):
    if not aadhaar:
        return ""

    return aadhaar.replace(" ", "").strip()


def normalize_pan(pan):
    if not pan:
        return ""

    return pan.strip().upper()


def compare_fields(document_type, extracted_fields, database_record):
    """
    Compare extracted document fields with the official database record.

    Returns:
        Dictionary containing comparison results.
    """

    if database_record is None:

        return {
            "record_found": False,
            "name_match": False,
            "dob_match": False,
            "aadhaar_match": None,
            "pan_match": None
        }

    comparison = {
        "record_found": True,
        "name_match": normalize_name(extracted_fields.get("name")) ==
                      normalize_name(database_record.get("name")),
        "dob_match": normalize_dob(extracted_fields.get("dob")) ==
                     normalize_dob(database_record.get("dob")),
        "aadhaar_match": None,
        "pan_match": None
    }

    if document_type == "aadhaar":
        comparison["aadhaar_match"] = (
            normalize_aadhaar(extracted_fields.get("aadhaar")) ==
            normalize_aadhaar(database_record.get("aadhaar"))
        )

    elif document_type == "pan":
        comparison["pan_match"] = (
            normalize_pan(extracted_fields.get("pan")) ==
            normalize_pan(database_record.get("pan"))
        )

    elif document_type == "application":
        comparison["aadhaar_match"] = (
            normalize_aadhaar(extracted_fields.get("aadhaar")) ==
            normalize_aadhaar(database_record.get("aadhaar"))
        )

        comparison["pan_match"] = (
            normalize_pan(extracted_fields.get("pan")) ==
            normalize_pan(database_record.get("pan"))
        )

    return comparison