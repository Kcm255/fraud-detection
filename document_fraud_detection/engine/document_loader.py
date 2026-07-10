# engine/document_loader.py

import os


UPLOAD_FOLDER = "uploads"


def find_document(base_name):
    """
    Searches for a document with supported extensions.

    Supported:
    - .png
    - .jpg
    - .jpeg
    - .pdf

    Returns:
        Full file path if found, otherwise None.
    """

    extensions = [".png", ".jpg", ".jpeg", ".pdf"]

    for ext in extensions:
        file_path = os.path.join(UPLOAD_FOLDER, base_name + ext)

        if os.path.exists(file_path):
            return file_path

    return None


def load_documents():
    """
    Locate the required documents inside the uploads folder.

    Returns:
        dict containing document paths.
    """

    documents = {
        "application": find_document("application_form"),
        "aadhaar": find_document("aadhaar"),
        "pan": find_document("pan")
    }

    return documents