# engine/database_lookup.py

import json
import os


DATABASE_PATH = "database/users.json"


def load_database():
    """
    Load all users from the JSON database.

    Returns:
        List of user records.
    """

    if not os.path.exists(DATABASE_PATH):
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    with open(DATABASE_PATH, "r", encoding="utf-8") as file:
        users = json.load(file)

    return users


def find_user(extracted_fields):
    """
    Find a user using Aadhaar first, then PAN.

    Parameters:
        extracted_fields (dict)

    Returns:
        Matching user dictionary or None.
    """

    users = load_database()

    aadhaar = extracted_fields.get("aadhaar")
    pan = extracted_fields.get("pan")

    # -----------------------------------
    # Search using Aadhaar
    # -----------------------------------

    if aadhaar:

        for user in users:

            if user.get("aadhaar") == aadhaar:
                return user

    # -----------------------------------
    # Search using PAN
    # -----------------------------------

    if pan:

        for user in users:

            if user.get("pan") == pan:
                return user

    # -----------------------------------

    return None